import datetime
import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dateutil.tz import tzutc
from pystac.extensions.raster import RasterBand

from .constants import ASSET_CLASSES, COG_RASTER_BAND, COG_TITLES, AssetType


@dataclass
class Metadata:
    """Asset-level metadata, all parsed from the filename."""

    asset_type: AssetType
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    tile: Optional[str]
    href: str

    @classmethod
    def from_href(cls, href: str) -> "Metadata":
        """Create a metadata object from a COG href."""

        parts = os.path.splitext(os.path.basename(href))[0].split("_")
        if len(parts) < 3:
            raise ValueError(f"Invalid CDL file name: {href}")
        if parts[2] == "cdls":
            asset_type = AssetType.Cropland
            start_datetime, end_datetime = _parse_year_into_datetimes(parts[0])
        elif parts[2] == "confidence":
            asset_type = AssetType.Confidence
            start_datetime, end_datetime = _parse_year_into_datetimes(parts[0])
        elif parts[1] == "cultivated":
            asset_type = AssetType.Cultivated
            start_datetime, end_datetime = _parse_year_into_datetimes(parts[0])
        elif not (parts[0] == "crop" and parts[1] == "frequency" and len(parts) >= 4):
            raise ValueError(f"Invalid CDL file name: {href}")
        else:
            if parts[2] == "corn":
                asset_type = AssetType.Corn
            elif parts[2] == "cotton":
                asset_type = AssetType.Cotton
            elif parts[2] == "soybeans":
                asset_type = AssetType.Soybeans
            elif parts[2] == "wheat":
                asset_type = AssetType.Wheat
            else:
                raise ValueError(f"Invalid CDL file name: {href}")
            start_datetime, end_datetime = _parse_year_range_into_datetimes(parts[3])

        if len(parts) > 4:
            tile = "_".join(parts[-3:])
        else:
            tile = None

        return cls(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            asset_type=asset_type,
            tile=tile,
            href=href,
        )

    @property
    def cog_profile(self) -> Dict[str, Any]:
        """Returns this asset's COG profile.

        If the data are classification information, this uses "mode" for
        overview_resampling -- otherwise, we use "average".
        """
        profile = {
            "compress": "deflate",
            "blocksize": 512,
            "driver": "COG",
        }
        if self.asset_type in (AssetType.Cropland, AssetType.Cultivated):
            profile["overview_resampling"] = "mode"
        else:
            profile["overview_resampling"] = "average"
        return profile

    @property
    def item_id(self) -> str:
        """Returns this asset's item-id.

        The id is constructed from the item type, the time descriptor, and the
        tile information (_not_ the asset type). This is how we link assets into
        the same item, e.g. frequency data, or cropland and confidence data.
        """
        item_id = f"{self.item_type}_{self.time_descriptor}"
        if self.tile:
            return f"{item_id}_{self.tile}"
        else:
            return item_id

    @property
    def item_type(self) -> str:
        """Returns this asset's item type.

        Both cropland and confidence data have a "cropland" item type. All
        frequency data (corn, soy, etc) have "frequency" item type.
        """
        if self.asset_type == AssetType.Confidence:
            return "cropland"
        elif self.asset_type.is_frequency():
            return "frequency"
        else:
            return self.asset_type.value

    @property
    def cog_title(self) -> str:
        """Returns this asset's title."""
        if self.asset_type.is_frequency():
            return (
                f"{COG_TITLES[self.asset_type]} "
                f"{self.start_datetime.year}-{self.end_datetime.year}"
            )
        else:
            return f"{COG_TITLES[self.asset_type]} {self.start_datetime.year}"

    @property
    def classes(self) -> Optional[List[Dict[str, Any]]]:
        """Returns this asset's classes."""
        return ASSET_CLASSES.get(self.asset_type)

    @property
    def raster_bands(self) -> List[RasterBand]:
        """Returns this asset's raster bands."""
        return [COG_RASTER_BAND[self.asset_type]]

    @property
    def time_descriptor(self) -> str:
        """Returns this asset's time descriptor.

        Usually this is just a year, but for the frequency data it's a range.
        """
        if self.asset_type.is_frequency():
            return f"{self.start_datetime.year}-{self.end_datetime.year}"
        else:
            return str(self.start_datetime.year)

    @property
    def stem(self) -> str:
        """Returns this asset's file name without an extension."""
        return Path(self.href).stem

    @property
    def colormap(self) -> Optional[Dict[int, Tuple[int, ...]]]:
        """Returns this asset's colormap, if it has classes."""
        classes = ASSET_CLASSES.get(self.asset_type)
        if classes:
            return dict(
                (
                    int(d["value"]),  # type: ignore
                    _color_hint_to_rgba(str(d["color_hint"])),
                )
                for d in classes
            )
        else:
            return None


def _parse_year_into_datetimes(
    year: str,
) -> Tuple[datetime.datetime, datetime.datetime]:
    year_as_int = int(year)
    return (
        datetime.datetime(year_as_int, 1, 1, tzinfo=tzutc()),
        datetime.datetime(year_as_int, 12, 31, 23, 59, 59, tzinfo=tzutc()),
    )


def _parse_year_range_into_datetimes(
    year_range: str,
) -> Tuple[datetime.datetime, datetime.datetime]:
    parts = year_range.split("-")
    if len(parts) != 2:
        raise ValueError(f"invalid year range: {year_range}")
    else:
        return (
            datetime.datetime(int(parts[0]), 1, 1, tzinfo=tzutc()),
            datetime.datetime(int(parts[1]), 12, 31, 23, 59, 59, tzinfo=tzutc()),
        )


def _color_hint_to_rgba(color_hint: str) -> Tuple[int, ...]:
    return tuple([*(int(color_hint[i : i + 2], 16) for i in (0, 2, 4)), 0])
