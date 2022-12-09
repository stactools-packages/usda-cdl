import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import stactools.core.create
from pystac import Asset, Collection, Item, MediaType
from pystac.extensions.item_assets import ItemAssetsExtension

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import COLLECTION_PROPS, CollectionType, Variable


@dataclass(frozen=True)
class Filename:
    variable: Variable
    year: int
    href: str

    @classmethod
    def parse(
        cls, href: str, expected_variable: Variable, expected_year: Optional[int] = None
    ) -> "Filename":
        """
        notes
        """
        id = os.path.splitext(os.path.basename(href))[0]
        parts = id.split("_")
        variable = Variable.from_str(parts[1])
        if variable != expected_variable:
            raise ValueError(f"expected '{expected_variable}, received '{variable}'")

        year = int(parts[2])
        if expected_year is not None and year != expected_year:
            raise ValueError(f"expected year '{expected_year}, got '{year}'")

        return cls(variable=variable, year=year, href=href)


def _add_asset(item: Item, filename: Filename) -> Item:
    asset_title = f"{constants.COG_ASSET_TITLES[filename.variable]} {filename.year}"
    asset = Asset(
        href=filename.href, title=asset_title, media_type=MediaType.COG, roles=["data"]
    )
    item.add_asset(filename.variable, asset)

    return item


def create_cropland_item(
    cropland_href: str, confidence_href: Optional[str] = None
) -> Item:
    """
    Creates a base STAC Item with COG assets for a single temporal unit.
    A temporal unit is year for the cropland collection.

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
    item.common_metadata.end_datetime = datetime(
        cropland_filename.year, 12, 31, 23, 59, 59
    )
    item.datetime = None
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    _add_asset(item, cropland_filename)

    if confidence_href is not None:
        confidence_filename = Filename.parse(
            confidence_href, Variable.Confidence, cropland_filename.year
        )
        _add_asset(item, confidence_filename)

    item.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)
    asset = item.assets[Variable.Cropland]
    asset.extra_fields["classification:classes"] = constants.COLLECTION_PROPS[
        CollectionType.CDL
    ]["classes"]

    return item


def create_cultivated_item(cultivated_href: str) -> Item:
    """
    Creates a base STAC Item with COG assets.

    Args:
        cultivated_href (str): Cultivated href to a COG

    Returns:
        Item: A STAC Item object.
    """

    item = stactools.core.create.item(cultivated_href)
    del item.assets["data"]

    cultivated_filename = Filename.parse(cultivated_href, Variable.Cultivated)
    _add_asset(item, cultivated_filename)

    item.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)
    asset = item.assets[Variable.Cultivated]
    asset.extra_fields["classification:classes"] = constants.COLLECTION_PROPS[
        CollectionType.Cultivated
    ]["classes"]

    return item


def create_frequency_item(
    corn_href: str,
    cotton_href: str,
    soybean_href: str,
    wheat_href: str,
) -> Item:
    """
    Creates a base STAC Item with COG assets.

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

    corn_filename = Filename.parse(corn_href, Variable.Corn)
    cotton_filename = Filename.parse(cotton_href, Variable.Cotton, corn_filename.year)
    soybean_filename = Filename.parse(
        soybean_href, Variable.Soybean, corn_filename.year
    )
    wheat_filename = Filename.parse(wheat_href, Variable.Wheat, corn_filename.year)

    item = _add_asset(item, corn_filename)
    item = _add_asset(item, cotton_filename)
    item = _add_asset(item, soybean_filename)
    item = _add_asset(item, wheat_filename)

    return item


def create_collection(collection_type: CollectionType) -> Collection:
    """
    Creates a STAC Collections for .

    Args:
        collection_type: Desired collection type for the STAC Collections.

    Returns:
        Collection: The created STAC Collections.
    """
    properties = COLLECTION_PROPS[collection_type]
    collection = Collection(
        id=properties["id"],
        title=properties["title"],
        description=properties["description"],
        keywords=constants.KEYWORDS,
        providers=constants.PROVIDERS,
        extent=properties["extent"],
    )

    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = properties["item_assets"]

    collection.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    collection.add_links([constants.LANDING_PAGE_LINK])

    return collection
