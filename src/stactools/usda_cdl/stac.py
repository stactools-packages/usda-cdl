import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import stactools.core.create
from pystac import Asset, Item, MediaType  # Add Collection later
#from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import Variable


@dataclass(frozen=True)
class Filename:
    variable: Variable
    year: int

    @classmethod
    def parse(cls, href: str, expected_variable: Variable) -> "Filename":
        """
        notes
        """
        id = os.path.splitext(os.path.basename(href))[0]
        parts = id.split("_")
        variable = parts[1]
        if variable != expected_variable:
            raise ValueError(
                f"expected '{expected_variable}, received '{variable}'"
            )

        year = int(parts[2])
        return cls(variable=variable, year=year)


def create_cropland_item(cropland_href: str, confidence_href: Optional[str] = None) -> Item:
    """
    Creates a base STAC Item with COG assets for a single temporal unit.
    A temporal unit is year for the base collection.

    Args:
        cropland_href (str): Cropland href to a COG.
        confidence_href (Callable[[str], str]): Confidence href to a COG.

    Returns:
        Item: A STAC Item object.
    """
    cropland_filename = Filename.parse(cropland_href, Variable.Cropland)

    item = stactools.core.create.item(cropland_href)
    del item.assets["data"]

    item.common_metadata.start_datetime = datetime(cropland_filename.year, 1, 1)
    item.common_metadata.end_datetime = datetime(cropland_filename.year, 12, 31, 23, 59, 59)
    item.datetime = None
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    asset_title = f"{constants.COG_ASSET_TITLES[cropland_filename.variable]} {cropland_filename.year}"
    asset = Asset(
        href=cropland_href,
        title=asset_title,
        media_type=MediaType.COG,
        roles=["data"]
    )
    item.add_asset(cropland_filename.variable, asset)

    if confidence_href is not None:
        confidence_filename = Filename.parse(confidence_href, Variable.Confidence)
        if confidence_filename.year != cropland_filename.year:
            raise ValueError(
                f"cropland year ({cropland_filename.year}) does not match "
                f"confidence year ({confidence_filename.year})")
        asset_title = f"{constants.COG_ASSET_TITLES[confidence_filename.variable]} {confidence_filename.year}"
        asset = Asset(
            href=confidence_href,
            title=asset_title,
            media_type=MediaType.COG,
            roles=["data"]
        )
        item.add_asset(confidence_filename.variable, asset)

    return item


def create_cultivated_item(
        cultivated_href: str) -> Item:
    """Creates a base STAC Item with COG assets for a single temporal unit.
       A temporal unit is year for the cultivated collection.

    Args:
        cultivated_href (str): Cultivated href to a COG

    Returns:
        Item: A STAC Item object.
    """
    cultivated_filename = Filename.parse(cultivated_href, Variable.Cultivated)

    item = stactools.core.create.item(cultivated_href)
    del item.assets["data"]

    asset_title = f"{constants.COG_ASSET_TITLES[cultivated_filename.variable]} {cultivated_filename.year}"
    asset = Asset(
        href=cultivated_href,
        title=asset_title,
        media_type=MediaType.COG,
        roles=["data"]
    )
    item.add_asset(cultivated_filename.variable, asset)

    return item


def create_frequency_item(
    corn_href: str,
    cotton_href: str,
    soybean_href: str,
    wheat_href: str,
) -> Item:
    """Creates a base STAC Item with COG assets for a single temporal unit.
       A temporal unit is year for the ancillary collection.

    Args:
        corn_href (str): Corn href to a COG
        cotton_href (str): Cotton href to a COG
        soybean_href (str): Soy href to a COG
        wheat_href (str): Wheat href to a COG

    Returns:
        Item: A STAC Item object.
    """
    item = stactools.core.create.item(corn_href)
    del item.assets["data"]

    item = _add_asset(item, corn_href, Variable.Corn)
    item = _add_asset(item, cotton_href, Variable.Cotton)
    item = _add_asset(item, soybean_href, Variable.Soybean)
    item = _add_asset(item, wheat_href, Variable.Wheat)

    return item


def _add_asset(item: Item, href: str, variable: Variable) -> Item:
    # TODO check year
    asset_title = f"{constants.COG_ASSET_TITLES[variable]}"
    asset = Asset(
        href=href,
        title=asset_title,
        media_type=MediaType.COG,
        roles=["data"]
    )
    item.add_asset(variable, asset)

    return item
