import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import stactools.core.create
from pystac import Asset, Collection, Item, MediaType
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.utils import make_absolute_href

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import Frequency, Variable
from stactools.usda_cdl.utils import cog_asset_dict, data_frequency


@dataclass(frozen=True)
class Filename:
    variable: Variable
    year: int

    @classmethod
    def parse(cls, href: str, expected_variable: Variable) -> "Filename":
        id = os.path.splitext(os.path.basename(href))[0]
        parts = id.split("_")
        variable = parts[1]
        if variable != expected_variable:
            raise ValueError(
                f"expected '{expected_variable}, received '{variable}'"
            )
    
        year = int(parts[2])
        return cls(variable=variable, year=year)


def create_base_item(cropland_href: str, confidence_href: Optional[str] = None) -> Item:
    """Creates a base STAC Item with COG assets for a single temporal unit.
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


def create_ancillary_item(
    cultivated_href: str, 
    corn_href: str, 
    cotton_href: str,
    wheat_href: str,
    soy_href: str) -> Item:
    """Creates a base STAC Item with COG assets for a single temporal unit.
       A temporal unit is year for the ancillary collection.

    Args:
        cultivated_href (str): Cultivated href to a COG
        corn_href (str): Corn href to a COG
        cotton_href (str): Cotton href to a COG
        wheat_href (str): Wheat href to a COG
        soy_href (str): Soy href to a COG

    Returns:
        Item: A STAC Item object.
    """
    id = os.path.splitext(os.path.basename(cultivated_href))[0]
    parts = id.split("_")
    variable = parts[1]
    cultivated_year = int(parts[2])

    item = stactools.core.create.item(cultivated_href)
    del item.assets["data"] 

    item.common_metadata.start_datetime = datetime(2021, 1, 1)
    item.common_metadata.end_datetime = datetime(2021, 12, 31, 23, 59, 59)
    item.datetime = None
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    asset_title = f"{constants.COG_ASSET_TITLES[variable]} {cultivated_year}"
    asset = Asset(
        href=cultivated_href,
        title=asset_title,
        media_type=MediaType.COG,
        roles=["data"]
    )
    item.add_asset(variable, asset) 
    

    nominal_datetime: Optional[datetime] = None
    if frequency == Frequency.USDA_CDL:
        id = basename[5:]
        year = int(id[0: 4])
        start_datetime = datetime(year, 1, 1)
        end_datetime = datetime(year, 12, 31, 23, 59, 59)
        nominal_datetime = start_datetime
    else:
        id = f"usda-cdl-{basename[-6:]}"
        year = int(id[-6: -2])
        start_datetime = datetime(2021, 1, 1)
        end_datetime = datetime(2021, 12, 31, 23, 59, 59)
        nominal_datetime = None

    item = stactools.core.create.item(cog_hrefs[Variable.Cropland])
    item.id = id
    item.datetime = nominal_datetime
    item.common_metadata.start_datetime = start_datetime
    item.common_metadata.end_datetime = end_datetime
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    item.assets.pop("data")
    for var in Variable:
        asset = cog_asset_dict(frequency, var)
        asset["href"] = make_absolute_href(cog_hrefs[var])
        item.add_asset(var.value, Asset.from_dict(asset))

    return item


def create_collection(frequency: Frequency) -> Collection:
    """Creates a STAC Collection for usda-cdl or usda-cdl-ancillary data.

    Args:
        collection (Collection): 'usda-cdl' or 'usda-cdl-ancillary'.

    Returns:
        Collection: A STAC collection for 'usda-cdl' or 'usda-cdl-ancillary' data.
    """
    if frequency == Frequency.USDA_CDL:
        collection = Collection(**constants.USDA_CDL_COLLECTION)

    else:
        collection = Collection(**constants.USDA_CDL_ANCILLARY_COLLECTION)

    collection.providers = constants.PROVIDERS

    item_assets = {}
    for var in Variable:
        item_assets[var.value] = AssetDefinition(cog_asset_dict(frequency, var))

    item_assets_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets_ext.item_assets = item_assets

    collection.stac_extensions.append(constants.RASTER_EXTENSION_V11)

    collection.add_link(constants.LANDING_PAGE_LINK)

    return collection
