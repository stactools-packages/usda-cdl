import datetime
from pathlib import Path
from typing import List

import pytest
from dateutil.tz import tzutc
from pystac import MediaType
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.raster import RasterExtension

from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import CLASSIFICATION_SCHEMA


def test_create_cdl_item(cdl: Path) -> None:
    item = stac.create_item(str(cdl))
    assert item.id == "cropland_2021"
    assert item.common_metadata.start_datetime == datetime.datetime(
        2021, 1, 1, tzinfo=tzutc()
    )
    assert item.common_metadata.end_datetime == datetime.datetime(
        2021, 12, 31, 23, 59, 59, tzinfo=tzutc()
    )
    assert item.extra_fields["usda_cdl:type"] == "cropland"

    assert len(item.assets) == 1
    asset = item.assets["cropland"]
    assert asset.title == "Cropland Data Layer (CDL) 2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    assert (
        "https://stac-extensions.github.io/classification/v1.1.0/schema.json"
        in item.stac_extensions
    )
    assert "classification:classes" in asset.extra_fields
    classes = asset.extra_fields["classification:classes"]
    assert classes

    _ = RasterExtension.ext(asset)

    item.validate()


def test_create_cdl_item_with_confidence(cdl: Path, confidence: Path) -> None:
    item = stac.create_item_from_hrefs([str(cdl), str(confidence)])
    assert item.id == "cropland_2021"
    assert item.extra_fields["usda_cdl:type"] == "cropland"

    assert len(item.assets) == 2
    asset = item.assets["confidence"]
    assert asset.title == "Confidence 2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]
    item.validate()


def test_create_cultivated_item(cultivated: Path) -> None:
    item = stac.create_item(str(cultivated))
    assert item.id == "cultivated_2021"
    assert item.extra_fields["usda_cdl:type"] == "cultivated"

    assert len(item.assets) == 1
    asset = item.assets["cultivated"]
    assert asset.title == "Cultivated 2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]


def test_create_frequency_item(
    corn: Path, cotton: Path, soybeans: Path, wheat: Path
) -> None:
    item = stac.create_item_from_hrefs(
        [str(corn), str(cotton), str(soybeans), str(wheat)]
    )
    assert item.id == "frequency_2008-2021"
    assert item.extra_fields["usda_cdl:type"] == "frequency"

    assert len(item.assets) == 4

    asset = item.assets["corn"]
    assert asset.title == "Corn 2008-2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    asset = item.assets["cotton"]
    assert asset.title == "Cotton 2008-2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    asset = item.assets["soybeans"]
    assert asset.title == "Soybeans 2008-2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    asset = item.assets["wheat"]
    assert asset.title == "Wheat 2008-2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    item.validate()


def test_create_collection() -> None:
    collection = stac.create_collection()

    _ = ItemAssetsExtension.ext(collection)
    assert CLASSIFICATION_SCHEMA in collection.stac_extensions

    collection.set_self_href("")
    collection.validate()


def test_create_cdl_tile_item(cdl_tile: Path) -> None:
    item = stac.create_item(str(cdl_tile))
    assert item.id == "cropland_2021_-91095_1807575_15000"
    item.validate()


def test_create_items_from_tiles(tiles: List[Path]) -> None:
    items = stac.create_items_from_tiles([str(p) for p in tiles])
    assert len(items) == 12
    for item in items:
        item.validate()


def test_cant_create_mismatched_item(cdl: Path, corn: Path) -> None:
    with pytest.raises(ValueError):
        stac.create_item_from_hrefs([str(cdl), str(corn)])
