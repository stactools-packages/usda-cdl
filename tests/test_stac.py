import datetime

from pystac import MediaType
from dateutil.tz import tzutc

import stactools.usda_cdl.stac

import pytest
from tests import test_data


def test_create_base_item_with_one_href() -> None:
    path = test_data.get_path("data-files/basic_cropland_2020.tif")
    item = stactools.usda_cdl.stac.create_base_item(path)
    assert item.common_metadata.start_datetime == datetime.datetime(2020, 1, 1, tzinfo=tzutc())
    assert item.common_metadata.end_datetime == datetime.datetime(
        2020, 12, 31, 23, 59, 59, tzinfo=tzutc())
    assert len(item.assets) == 1
    asset = item.assets["cropland"]
    assert asset.title == "Cropland Data Layer (CDL) 2020"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]
    item.validate()


def test_create_base_item_with_one_href_2021() -> None:
    path = test_data.get_path("data-files/basic_cropland_2021.tif")
    item = stactools.usda_cdl.stac.create_base_item(path)
    assert item.common_metadata.start_datetime == datetime.datetime(2021, 1, 1, tzinfo=tzutc())
    assert item.common_metadata.end_datetime == datetime.datetime(
        2021, 12, 31, 23, 59, 59, tzinfo=tzutc())


def test_create_base_item_with_two_hrefs() -> None:
    cropland_path = test_data.get_path("data-files/basic_cropland_2020.tif")
    confidence_path = test_data.get_path("data-files/basic_confidence_2020.tif")
    item = stactools.usda_cdl.stac.create_base_item(cropland_path, confidence_path)
    assert len(item.assets) == 2
    asset = item.assets["confidence"]
    assert asset.title == "Confidence 2020"
    assert asset.media_type == MediaType.COG
    assert asset.roles == ["data"]
    item.validate()


def test_create_base_item_two_different_years() -> None:
    cropland_path = test_data.get_path("data-files/basic_cropland_2020.tif")
    confidence_path = test_data.get_path("data-files/basic_confidence_2021.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_base_item(cropland_path, confidence_path)


def test_create_base_item_with_incorrect_cropland_href() -> None:
    path = test_data.get_path("data-files/basic_confidence_2020.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_base_item(path)


def test_create_base_item_with_incorrect_confidence_href() -> None:
    path = test_data.get_path("data-files/basic_cropland_2020.tif")
    with pytest.raises(ValueError):
        stactools.usda_cdl.stac.create_base_item(path, path)
