import os
from datetime import datetime, timezone
from typing import Dict, Optional

import stactools.core.create
from pystac import Asset, Collection, Item
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.utils import make_absolute_href

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import Frequency, Variable
from stactools.usda_cdl.utils import cog_asset_dict, data_frequency


def create_basic_item(cog_hrefs: Dict[Variable, str]) -> Item:
    """Creates a STAC Item with COG assets for a single temporal unit.

    A temporal unit is year for the usda_cdl collection.

    Args:
        cog_hrefs (Dict[Variable, str]): A dictionary mapping variables (keys) to
            COG HREFs (values).

    Returns:
        Item: A STAC Item.
    """
    frequency = data_frequency(cog_hrefs[Variable.Cropland])  # collection
    basename = os.path.splitext(os.path.basename(cog_hrefs[Variable.Cropland]))[
        0
    ]  # asset

    nominal_datetime: Optional[datetime] = None
    if frequency == Frequency.USDA_CDL:
        id = basename[5:]
        year = int(id[0:4])
        start_datetime = datetime(year, 1, 1)
        end_datetime = datetime(year, 12, 31, 23, 59, 59)
        nominal_datetime = start_datetime
    else:
        id = f"usda-cdl-{basename[-6:]}"
        year = int(id[-6:-2])
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

def create_ancillary_item(cog_hrefs: Dict[Variable, str]) -> Item:
    """Creates a STAC Item with COG assets for a single temporal unit.

    A temporal unit is year for the usda_cdl collection.

    Args:
        cog_hrefs (Dict[Variable, str]): A dictionary mapping variables (keys) to
            COG HREFs (values).

    Returns:
        Item: A STAC Item.
    """
    frequency = data_frequency(cog_hrefs[Variable.Cropland])  # collection
    basename = os.path.splitext(os.path.basename(cog_hrefs[Variable.Cropland]))[
        0
    ]  # asset

    nominal_datetime: Optional[datetime] = None
    if frequency == Frequency.USDA_CDL:
        id = basename[5:]
        year = int(id[0:4])
        start_datetime = datetime(year, 1, 1)
        end_datetime = datetime(year, 12, 31, 23, 59, 59)
        nominal_datetime = start_datetime
    else:
        id = f"usda-cdl-{basename[-6:]}"
        year = int(id[-6:-2])
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
