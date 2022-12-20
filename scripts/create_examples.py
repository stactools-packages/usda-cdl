#!/usr/bin/env python3

from pathlib import Path

from pystac import CatalogType

from stactools.usda_cdl import stac

root = Path(__file__).parents[1]
examples = root / "examples"
tiles = root / "tests" / "data-files" / "tiles"

collection = stac.create_collection()
items = stac.create_items_from_tiles([str(p) for p in tiles.glob("*.tif")])
collection.add_items(items)

collection.normalize_hrefs(str(examples))
collection.make_all_asset_hrefs_relative()
collection.save(catalog_type=CatalogType.SELF_CONTAINED)
