#!/usr/bin/env python3

from pathlib import Path

from pystac import CatalogType

from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import COLLECTION_ID, AssetType

root = Path(__file__).parents[1]
examples = root / "examples"
data_files = root / "tests" / "data-files"

collection = stac.create_collection(COLLECTION_ID)
for item_type in AssetType:
    if item_type == AssetType.Cropland:
        item = stac.create_cropland_item(
            str(data_files / "basic_cropland_2019.tif"),
        )
    elif item_type == AssetType.Corn:
        item = stac.create_frequency_item(
            str(data_files / "frequency_corn_2021.tif"),
            str(data_files / "frequency_cotton_2021.tif"),
            str(data_files / "frequency_soybean_2021.tif"),
            str(data_files / "frequency_wheat_2021.tif"),
        )
    elif item_type == AssetType.Cultivated:
        item = stac.create_cultivated_item(
            str(data_files / "ancillary_cultivated_2021.tif")
        )
    collection.add_item(item)

collection.normalize_hrefs(str(examples))
collection.make_all_asset_hrefs_relative()
collection.save(catalog_type=CatalogType.SELF_CONTAINED)
