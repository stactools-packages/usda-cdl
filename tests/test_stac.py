import datetime

import pytest
from dateutil.tz import tzutc
from pystac import MediaType

import stactools.usda_cdl.stac
from stactools.usda_cdl.constants import CollectionType
from tests import test_data


def test_create_cropland_item_with_one_href() -> None:
    path = test_data.get_path("data-files/basic_cropland_2020.tif")
    item = stactools.usda_cdl.stac.create_cropland_item(path)
    assert item.common_metadata.start_datetime == datetime.datetime(
        2020, 1, 1, tzinfo=tzutc()
    )
    assert item.common_metadata.end_datetime == datetime.datetime(
        2020, 12, 31, 23, 59, 59, tzinfo=tzutc()
    )
    assert len(item.assets) == 1
    asset = item.assets["cropland"]
    assert asset.title == "Cropland Data Layer (CDL) 2020"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    assert "https://stac-extensions.github.io/classification/v1.1.0/schema.json" in item.stac_extensions
    assert "classification:classes" in asset.extra_fields
    classes = asset.extra_fields["classification:classes"]
    assert classes

    item.validate()


def test_create_cropland_item_with_one_href_2021() -> None:
    path = test_data.get_path("data-files/basic_cropland_2021.tif")
    item = stactools.usda_cdl.stac.create_cropland_item(path)
    assert item.common_metadata.start_datetime == datetime.datetime(
        2021, 1, 1, tzinfo=tzutc()
    )
    assert item.common_metadata.end_datetime == datetime.datetime(
        2021, 12, 31, 23, 59, 59, tzinfo=tzutc()
    )


def test_create_cropland_item_with_two_hrefs() -> None:
    cropland_path = test_data.get_path("data-files/basic_cropland_2020.tif")
    confidence_path = test_data.get_path("data-files/basic_confidence_2020.tif")
    item = stactools.usda_cdl.stac.create_cropland_item(cropland_path, confidence_path)
    assert len(item.assets) == 2
    asset = item.assets["confidence"]
    assert asset.title == "Confidence 2020"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]
    item.validate()


def test_create_cropland_item_two_different_years() -> None:
    cropland_path = test_data.get_path("data-files/basic_cropland_2020.tif")
    confidence_path = test_data.get_path("data-files/basic_confidence_2021.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_cropland_item(cropland_path, confidence_path)


def test_create_cropland_item_with_incorrect_cropland_href() -> None:
    path = test_data.get_path("data-files/basic_confidence_2020.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_cropland_item(path)


def test_create_cropland_item_with_incorrect_confidence_href() -> None:
    path = test_data.get_path("data-files/basic_cropland_2020.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_cropland_item(path, path)


def test_create_cultivated_item_with_one_href() -> None:
    path = test_data.get_path("data-files/ancillary_cultivated_2021.tif")
    item = stactools.usda_cdl.stac.create_cultivated_item(path)
    assert len(item.assets) == 1
    asset = item.assets["cultivated"]
    assert asset.title == "Cultivated 2021"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]

    assert "https://stac-extensions.github.io/classification/v1.1.0/schema.json" in item.stac_extensions
    assert "classification:classes" in asset.extra_fields
    classes = asset.extra_fields["classification:classes"]
    assert classes

    item.validate()


def test_create_frequency_item_with_four_href() -> None:
    corn_path = test_data.get_path("data-files/frequency_corn_2021.tif")
    cotton_path = test_data.get_path("data-files/frequency_cotton_2021.tif")
    soybean_path = test_data.get_path("data-files/frequency_soybean_2021.tif")
    wheat_path = test_data.get_path("data-files/frequency_wheat_2021.tif")
    item = stactools.usda_cdl.stac.create_frequency_item(
        corn_path, cotton_path, soybean_path, wheat_path
    )
    assert len(item.assets) == 4
    item.validate()


def test_create_frequency_item_different_years() -> None:
    corn_path = test_data.get_path("data-files/frequency_corn_2020.tif")
    cotton_path = test_data.get_path("data-files/frequency_cotton_2021.tif")
    soybean_path = test_data.get_path("data-files/frequency_soybean_2021.tif")
    wheat_path = test_data.get_path("data-files/frequency_wheat_2021.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_frequency_item(
            corn_path, cotton_path, soybean_path, wheat_path
        )


def test_create_cdl_collection() -> None:
    collection = stactools.usda_cdl.stac.create_collection(CollectionType.CDL)
    assert collection.id == "usda-cdl"
    collection.set_self_href("")
    collection.validate()


def test_create_cultivated_collection() -> None:
    collection = stactools.usda_cdl.stac.create_collection(CollectionType.Cultivated)
    assert collection.id == "usda-cdl-cultivated"
    collection.set_self_href("")
    collection.validate()


def test_create_frequency_collection() -> None:
    collection = stactools.usda_cdl.stac.create_collection(CollectionType.Frequency)
    assert collection.id == "usda-cdl-frequency"
    collection.set_self_href("")
    collection.validate()
