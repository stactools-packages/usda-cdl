#!/usr/bin/env python3

from pathlib import Path

from pystac import Catalog, CatalogType

from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import CollectionType

root = Path(__file__).parents[1]
examples = root / "examples"
data_files = root / "tests" / "data-files"

catalog = Catalog(id="usda-cdl", description="An example catalog for USDA CDL data")
for collection_type in CollectionType:
    collection = stac.create_collection(collection_type)
    catalog.add_child(collection)
    if collection_type == CollectionType.CDL:
        item = stac.create_cropland_item(str(data_files / "basic_cropland_2019.tif"))
    elif collection_type == CollectionType.Frequency:
        item = stac.create_frequency_item(
            str(data_files / "frequency_corn_2021.tif"),
            str(data_files / "frequency_cotton_2021.tif"),
            str(data_files / "frequency_soybean_2021.tif"),
            str(data_files / "frequency_wheat_2021.tif"),
        )
    elif collection_type == CollectionType.Cultivated:
        item = stac.create_cultivated_item(str(data_files / "ancillary_cultivated_2021.tif"))
    collection.add_item(item)

catalog.normalize_hrefs(str(examples))
catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=CatalogType.SELF_CONTAINED)
