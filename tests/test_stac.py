from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import Frequency, Variable
from tests import test_data


def test_create_single_item() -> None:
    cog_hrefs = {
        Variable.Cropland: test_data.get_path("data-files/usda_cdl_cropland_2021.tif"),
        Variable.Confidence: test_data.get_path("data-files/usda_cdl_confidence_2021.tif")
    }
    item = stac.create_basic_items(cog_hrefs)
    assert item.id == "x"
    assert len(item.assets) == 4
    item.validate()

def test_create_single_item() -> None:
    cog_hrefs = {
        Variable.Cultivated: test_data.get_path("data-files/usda_cdl_ancillary_cultivated_2020.tif"),
        Variable.Frequency_Corn: test_data.get_path("data-files/"),
        Variable.Frequency_Cotton: test_data.get_path("data-files/"),
        Variable.Frequency_Wheat: test_data.get_path("data-files/"),
        Variable.Frequency_Soybean: test_data.get_path("data-files/"),
    }
    item = stac.create_ancillary_items(cog_hrefs)
    assert item.id == "x"
    assert len(item.assets) == 4
    item.validate()


def test_usda_cdl_collection() -> None:
    collection = stac.create_collection(Frequency.USDA_CDL)
    collection_dict = collection.to_dict()
    assert collection.id == "usda-cdl"
    assert collection_dict["item_assets"]["cropland"]["title"].startswith("CDL")
    assert len(collection_dict["item_assets"]) == 8


def test_usda_cdl_ancillary_collection() -> None:
    collection = stac.create_collection(Frequency.USDA_CDL_ANCILLARY)
    collection_dict = collection.to_dict()
    assert collection.id == "usda-cdl-ancillary"
    assert collection_dict["item_assets"]["cropland"]["title"].startswith(
        "CDL_Ancillary"
    )
    assert len(collection_dict["item_assets"]) == 4
