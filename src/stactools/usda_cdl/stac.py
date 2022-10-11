import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import stactools.core.create
from pystac import Asset, Item, Collection, MediaType  # Add Collection later
<<<<<<< HEAD
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
=======
#from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
>>>>>>> a4346a7314f25e4615f77f7600f007789c6eca00

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import Variable, CollectionType, COLLECTION_PROPS



@dataclass(frozen=True)
class Filename:
    variable: Variable
    year: int
    href: str

    @classmethod
    def parse(cls, href: str, expected_variable: Variable, expected_year: Optional[int] = None) -> "Filename":
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
        if expected_year is not None and year != expected_year:
            raise ValueError(
                f"expected year '{expected_year}, got '{year}'"
            )

        return cls(variable=variable, year=year, href=href)


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

    _add_asset(item, cropland_filename)

    if confidence_href is not None:
        confidence_filename = Filename.parse(confidence_href, Variable.Confidence, cropland_filename.year)
        _add_asset(item, confidence_filename)

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

    item = stactools.core.create.item(cultivated_href)
    del item.assets["data"]

    cultivated_filename = Filename.parse(cultivated_href, Variable.Cultivated)
    _add_asset(item, cultivated_filename)

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

    corn_filename = Filename.parse(corn_href, Variable.Corn)
    cotton_filename = Filename.parse(cotton_href, Variable.Cotton, corn_filename.year)
    soybean_filename = Filename.parse(soybean_href, Variable.Soybean, corn_filename.year)
    wheat_filename = Filename.parse(wheat_href, Variable.Wheat, corn_filename.year)

    item = _add_asset(item, corn_filename)
    item = _add_asset(item, cotton_filename)
    item = _add_asset(item, soybean_filename)
    item = _add_asset(item, wheat_filename)

    return item


def _add_asset(item: Item, filename: Filename) -> Item:
    asset_title = f"{constants.COG_ASSET_TITLES[filename.variable]} {filename.year}"
    asset = Asset(
        href=filename.href,
        title=asset_title,
        media_type=MediaType.COG,
        roles=["data"]
    )
    item.add_asset(filename.variable, asset)

    return item

<<<<<<< HEAD
def create_collection(collection_type: CollectionType) -> Collection:
=======
def create_collection(collection_id: str) -> Collection:
>>>>>>> a4346a7314f25e4615f77f7600f007789c6eca00
    """
    Creates a STAC Collection for CDL. 

    Args:
        collection_id (str): Desired ID for the STAC Collection.
    Returns:
        Collection: The created STAC Collection.
    """
<<<<<<< HEAD
    properties = COLLECTION_PROPS[collection_type]
    collection = Collection(
                id=properties["id"],
                title = properties["title"],
                description=properties["description"],
                keywords=constants.KEYWORDS,
                providers=constants.PROVIDERS,
                extent=properties["extent"],
    )
=======
    collection = Collection(id=collection_id,
                title=constants.COLLECTION_TITLE,
                description=constants.COLLECTION_DESCRIPTION,
                license=constants.LICENSE,
                keywords=constants.KEYWORDS,
                providers=constants.PROVIDERS,
                extent=constants.EXTENT,
                summaries=constants.SUMMARIES,
                extra_fields={
                    "esa_worldcover:product_version":
                    constants.PRODUCT_VERSION
                })
>>>>>>> a4346a7314f25e4615f77f7600f007789c6eca00
    #scientific = ScientificExtension.ext(collection, add_if_missing=True)
    #scientific.doi = constants.DATA_DOI
    #scientific.citation = constants.DATA_CITATION

    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
<<<<<<< HEAD
    item_assets.item_assets = properties["item_assets"]
=======
    item_assets.item_assets = constants.ITEM_ASSETS
>>>>>>> a4346a7314f25e4615f77f7600f007789c6eca00

    #RasterExtension.add_to(collection)
    collection.stac_extensions.append(constants.CLASSIFICATION_SCHEMA)

    #collection.add_links([
        #constants.LICENSE_LINK, constants.USER_LINK, constants.VALIDATION_LINK
    # ])

    return collection