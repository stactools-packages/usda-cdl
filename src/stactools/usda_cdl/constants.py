from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Type, TypeVar

from pystac import (
    Extent,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    SpatialExtent,
    TemporalExtent,
)
from pystac.extensions.item_assets import AssetDefinition

T = TypeVar("T", bound="StrEnum")


class StrEnum(str, Enum):
    @classmethod
    def from_str(cls: Type[T], s: str) -> T:
        for value in cls:
            if value == s:
                return value
        raise ValueError(f"Could not parse value from string: {s}")


class Variable(StrEnum):
    Cropland = "cropland"
    Confidence = "confidence"
    Cultivated = "cultivated"
    Corn = "corn"
    Cotton = "cotton"
    Soybean = "soybean"
    Wheat = "wheat"


class CollectionType(StrEnum):
    CDL = "cdl"
    Cultivated = "cultivated"
    Frequency = "frequency"


CLASSIFICATION_SCHEMA = (
    "https://stac-extensions.github.io/classification/v1.1.0/schema.json"
)
COG_ASSET_TITLES = {
    Variable.Cropland: "Cropland Data Layer (CDL)",
    Variable.Confidence: "Confidence",
    Variable.Cultivated: "Cultivated",
    Variable.Corn: "Corn",
    Variable.Cotton: "Cotton",
    Variable.Soybean: "Soybean",
    Variable.Wheat: "Wheat",
}
COG_ROLES = ["data"]
COG_RASTER_BANDS = {
    Variable.Cropland: [
        {
            "data_type": "uint8",
            "nodata": "0",
            "spatial_resolution": 30,
        }
    ],
    Variable.Confidence: [
        {
            "data_type": "uint8",
            "spatial_resolution": 30,
        }
    ],
    Variable.Cultivated: [
        {
            "data_type": "uint8",
            "nodata": "0",
            "spatial_resolution": 30,
        }
    ],
    Variable.Corn: [
        {
            "data_type": "uint8",
            "nodata": "255",
            "spatial_resolution": 30,
        }
    ],
    Variable.Cotton: [
        {
            "data_type": "uint8",
            "nodata": "255",
            "spatial_resolution": 30,
        }
    ],
    Variable.Soybean: [
        {
            "data_type": "uint8",
            "nodata": "255",
            "spatial_resolution": 30,
        }
    ],
    Variable.Wheat: [
        {
            "data_type": "uint8",
            "nodata": "255",
            "spatial_resolution": 30,
        }
    ],
}
# RASTER_EXTENSION_V11 = "https://stac-extensions.github.io/raster/v1.1.0/schema.json"

LANDING_PAGE_LINK = Link(
    rel="about",
    target=("https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php"),
    title="Product Landing Page",
)

PROVIDERS = [
    Provider(
        name="United States Department of Agriculture - National Agricultural Statistics Service",
        roles=[ProviderRole.PRODUCER, ProviderRole.LICENSOR],
        url="https://www.nass.usda.gov/",
    )
]

KEYWORDS = [
    "Land Cover",
    "Land Use",
    "USDA",
    "Agriculture",
]

COLLECTION_PROPS: Dict[str, Any] = {
    CollectionType.CDL: {
        "id": "usda-cdl",
        "title": "USDA Cropland Data Layer (CDL)",
        "description": "The USDA Cropland Data Layer (CDL) is a crop-specific land cover data "
        "layer. The Confidence Layer represents the predicted confidence that is associated "
        "with an output pixel. A value of zero would therefore have a low confidence, "
        "while a value of 100 would have a very high confidence.",
        "extent": Extent(
            SpatialExtent([[-127.887, -74.158, 47.9580, 23.1496]]),
            TemporalExtent([[datetime(2008, 1, 1, tzinfo=timezone.utc), None]]),
        ),
        "item_assets": {
            "cropland": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            )
        },
        "classes": [
            {"value": 1, "description": "Corn", "color_hint": "FFD200"},
            {"value": 2, "description": "Cotton", "color_hint": "FF2525"},
            {"value": 3, "description": "Rice", "color_hint": "00A8E3"},
            {"value": 4, "description": "Sorghum", "color_hint": "FF9E0A"},
            {"value": 5, "description": "Soybeans", "color_hint": "256F00"},
            {"value": 6, "description": "Sunflower", "color_hint": "FFFF00"},
            {"value": 10, "description": "Peanuts", "color_hint": "6FA400"},
            {"value": 11, "description": "Tobacco", "color_hint": "00AE4A"},
            {"value": 12, "description": "Sweet Corn", "color_hint": "DDA40A"},
            {"value": 13, "description": "Pop or Orn Corn", "color_hint": "DDA40A"},
            {"value": 14, "description": "Mint", "color_hint": "7DD2FF"},
            {"value": 21, "description": "Barley", "color_hint": "E1007B"},
            {"value": 22, "description": "Durum Wheat", "color_hint": "886153"},
            {"value": 23, "description": "Spring Wheat", "color_hint": "D7B56B"},
            {"value": 24, "description": "Winter Wheat", "color_hint": "A46F00"},
            {"value": 25, "description": "Other Small Grains", "color_hint": "D59EBB"},
            {"value": 26, "description": "Winter Wheat/Soybeans", "color_hint": "6F6F00"},
            {"value": 27, "description": "Rye", "color_hint": "AC007B"},
            {"value": 28, "description": "Oats", "color_hint": "9F5888"},
            {"value": 29, "description": "Millet", "color_hint": "6F0048"},
            {"value": 30, "description": "Speltz", "color_hint": "D59EBB"},
            {"value": 31, "description": "Canola", "color_hint": "D1FF00"},
            {"value": 32, "description": "Flaxseed", "color_hint": "7D99FF"},
            {"value": 33, "description": "Safflower", "color_hint": "D5D500"},
            {"value": 34, "description": "Rape Seed", "color_hint": "D1FF00"},
            {"value": 35, "description": "Mustard", "color_hint": "00AE4A"},
            {"value": 36, "description": "Alfalfa", "color_hint": "FFA4E1"},
            {"value": 37, "description": "Other Hay/Non Alfalfa", "color_hint": "A4F18B"},
            {"value": 38, "description": "Camelina", "color_hint": "00AE4A"},
            {"value": 39, "description": "Buckwheat", "color_hint": "D59EBB"},
            {"value": 41, "description": "Sugarbeets", "color_hint": "A800E3"},
            {"value": 42, "description": "Dry Beans", "color_hint": "A40000"},
            {"value": 43, "description": "Potatoes", "color_hint": "6F2500"},
            {"value": 44, "description": "Other Crops", "color_hint": "00AE4A"},
            {"value": 45, "description": "Sugarcane", "color_hint": "B07DFF"},
            {"value": 46, "description": "Sweet Potatoes", "color_hint": "6F2500"},
            {"value": 47, "description": "Misc. Vegs & Fruits", "color_hint": "FF6666"},
            {"value": 48, "description": "Watermelons", "color_hint": "FF6666"},
            {"value": 49, "description": "Onions", "color_hint": "FFCC66"},
            {"value": 50, "description": "Cucumbers", "color_hint": "FF6666"},
            {"value": 51, "description": "Chick Peas", "color_hint": "00AE4A"},
            {"value": 52, "description": "Lentils", "color_hint": "00DDAE"},
            {"value": 53, "description": "Peas", "color_hint": "53FF00"},
            {"value": 54, "description": "Tomatoes", "color_hint": "F1A277"},
            {"value": 55, "description": "Caneberries", "color_hint": "FF6666"},
            {"value": 56, "description": "Hops", "color_hint": "00AE4A"},
            {"value": 57, "description": "Herbs", "color_hint": "7DD2FF"},
            {"value": 58, "description": "Clover/Wildflowers", "color_hint": "E8BEFF"},
            {"value": 59, "description": "Sod/Grass Seed", "color_hint": "AEFFDD"},
            {"value": 60, "description": "Switchgrass", "color_hint": "00AE4A"},
            {"value": 61, "description": "Fallow/Idle Cropland", "color_hint": "BEBE77"},
            {"value": 63, "description": "Forest", "color_hint": "92CC92"},
            {"value": 64, "description": "Shrubland", "color_hint": "C5D59E"},
            {"value": 65, "description": "Barren", "color_hint": "CCBEA2"},
            {"value": 66, "description": "Cherries", "color_hint": "FF00FF"},
            {"value": 67, "description": "Peaches", "color_hint": "FF8EAA"},
            {"value": 68, "description": "Apples", "color_hint": "B9004F"},
            {"value": 69, "description": "Grapes", "color_hint": "6F4488"},
            {"value": 70, "description": "Christmas Trees", "color_hint": "007777"},
            {"value": 71, "description": "Other Tree Crops", "color_hint": "B09A6F"},
            {"value": 72, "description": "Citrus", "color_hint": "FFFF7D"},
            {"value": 74, "description": "Pecans", "color_hint": "B56F5B"},
            {"value": 75, "description": "Almonds", "color_hint": "00A482"},
            {"value": 76, "description": "Walnuts", "color_hint": "E9D5AE"},
            {"value": 77, "description": "Pears", "color_hint": "B09A6F"},
            {"value": 81, "description": "Clouds/No Data", "color_hint": "F1F1F1"},
            {"value": 82, "description": "Developed", "color_hint": "9A9A9A"},
            {"value": 83, "description": "Water", "color_hint": "4A6fA2"},
            {"value": 87, "description": "Wetlands", "color_hint": "7DB0B0"},
            {"value": 88, "description": "Nonag/Undefined", "color_hint": "E8FFBE"},
            {"value": 92, "description": "Aquaculture", "color_hint": "00FFFF"},
            {"value": 111, "description": "Open Water", "color_hint": "4A6FA2"},
            {"value": 112, "description": "Perennial Ice/Snow", "color_hint": "D2E1F8"},
            {"value": 121, "description": "Developed/Open Space", "color_hint": "9A9A9A"},
            {"value": 122, "description": "Developed/Low Intensity", "color_hint": "9A9A9A"},
            {"value": 123, "description": "Developed/Med Intensity", "color_hint": "9A9A9A"},
            {"value": 124, "description": "Developed/High Intensity", "color_hint": "9A9A9A"},
            {"value": 131, "description": "Barren", "color_hint": "CCBEA2"},
            {"value": 141, "description": "Deciduous Forest", "color_hint": "92CC92"},
            {"value": 142, "description": "Evergreen Forest", "color_hint": "92CC92"},
            {"value": 143, "description": "Mixed Forest", "color_hint": "92CC92"},
            {"value": 152, "description": "Shrubland", "color_hint": "C5D59E"},
            {"value": 176, "description": "Grassland/Pasture", "color_hint": "E8FFBE"},
            {"value": 190, "description": "Woody Wetlands", "color_hint": "7DB0B0"},
            {"value": 195, "description": "Herbaceous Wetlands", "color_hint": "7DB0B0"},
            {"value": 204, "description": "Pistachios", "color_hint": "00FF8B"},
            {"value": 205, "description": "Triticale", "color_hint": "D59EBB"},
            {"value": 206, "description": "Carrots", "color_hint": "FF6666"},
            {"value": 207, "description": "Asparagus", "color_hint": "FF6666"},
            {"value": 208, "description": "Garlic", "color_hint": "FF6666"},
            {"value": 209, "description": "Cantaloupes", "color_hint": "FF6666"},
            {"value": 210, "description": "Prunes", "color_hint": "FF8EAA"},
            {"value": 211, "description": "Olives", "color_hint": "334833"},
            {"value": 212, "description": "Oranges", "color_hint": "E36F25"},
            {"value": 213, "description": "Honeydew Melons", "color_hint": "FF6666"},
            {"value": 214, "description": "Broccoli", "color_hint": "FF6666"},
            {"value": 215, "description": "Avocados", "color_hint": "66994B"},
            {"value": 216, "description": "Peppers", "color_hint": "FF6666"},
            {"value": 217, "description": "Pomegranates", "color_hint": "B09A6F"},
            {"value": 218, "description": "Nectarines", "color_hint": "FF8EAA"},
            {"value": 219, "description": "Greens", "color_hint": "FF6666"},
            {"value": 220, "description": "Plums", "color_hint": "FF8EAA"},
            {"value": 221, "description": "Strawberreis", "color_hint": "FF6666"},
            {"value": 222, "description": "Squash", "color_hint": "FF6666"},
            {"value": 223, "description": "Apricots", "color_hint": "FF8EAA"},
            {"value": 224, "description": "Vetch", "color_hint": "00AE4A"},
            {"value": 225, "description": "Winter Wheat/Corn", "color_hint": "FFD200"},
            {"value": 226, "description": "Oats/Corn", "color_hint": "FFD200"},
            {"value": 227, "description": "Lettuce", "color_hint": "FF6666"},
            {"value": 228, "description": "Triticale/Corn", "color_hint": "FF6666"},
            {"value": 229, "description": "Pumpkins", "color_hint": "FF6666"},
            {"value": 230, "description": "Lettuce/Durum Wheat", "color_hint": "886153"},
            {"value": 231, "description": "Lettuce/Cataloupe", "color_hint": "FF6666"},
            {"value": 232, "description": "Lettuce/Cotton", "color_hint": "FF2525"},
            {"value": 233, "description": "Lettuce/Barley", "color_hint": "A1007B"},
            {"value": 234, "description": "Durum Wheat/Sorghum", "color_hint": "FF9E0A"},
            {"value": 235, "description": "Barley/Sorghum", "color_hint": "FF9E0A"},
            {"value": 236, "description": "Winter Wheat/Sorghum", "color_hint": "A46F00"},
            {"value": 237, "description": "Barley/Corn", "color_hint": "FFD200"},
            {"value": 238, "description": "Winter Wheat/Cotton", "color_hint": "A46F00"},
            {"value": 239, "description": "Soybeans/Cotton", "color_hint": "256F00"},
            {"value": 240, "description": "Soybeans/Oats ", "color_hint": "256F00"},
            {"value": 241, "description": "Corn/Soybeans", "color_hint": "FFD200"},
            {"value": 242, "description": "Blueberries", "color_hint": "000099"},
            {"value": 243, "description": "Cabbage", "color_hint": "FF6666"},
            {"value": 244, "description": "Cauliflower", "color_hint": "FF6666"},
            {"value": 245, "description": "Celery", "color_hint": "FF6666"},
            {"value": 246, "description": "Radishes", "color_hint": "FF6666"},
            {"value": 247, "description": "Turnips", "color_hint": "FF6666"},
            {"value": 248, "description": "Eggplants", "color_hint": "FF6666"},
            {"value": 249, "description": "Gourds", "color_hint": "FF6666"},
            {"value": 250, "description": "Cranberries", "color_hint": "FF6666"},
            {"value": 254, "description": "Barley/Soybeans", "color_hint": "256F00"},
        ],
    },
    CollectionType.Cultivated: {
        "id": "usda-cdl-cultivated",
        "title": "USDA CDL Cultivated",
        "description": "The UDSA CDL Cultivated Layer is based on five years (2017-2021).",
        "extent": Extent(
            SpatialExtent([[-127.887, -74.158, 47.9580, 23.1496]]),
            TemporalExtent([[datetime(2021, 1, 1, tzinfo=timezone.utc), None]]),
        ),
        "item_assets": {
            "cultivated": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            )
        },
        "classes": [
            {"value": 1, "description": "Non-Cultivated", "color-hint": "000000"},
            {"value": 2, "description": "Cultivated", "color-hint": "006300"},
        ],
    },
    CollectionType.Frequency: {
        "id": "usda-cdl-frequency",
        "title": "USDA CDL Frequnecy",
        "description": "The USDA CDL 2021 Crop Frequency Layer identifies crop specific "
        "planting frequency and are based on land cover information derived from the "
        "2008 through 2021 CDL's. There are currently four individual crop frequency "
        "data layers that represent four major crops: corn, cotton, soybeans, and wheat.",
        "extent": Extent(
            SpatialExtent([[-127.887, -74.158, 47.9580, 23.1496]]),
            TemporalExtent([[datetime(2021, 1, 1, tzinfo=timezone.utc), None]]),
        ),
        "item_assets": {
            "corn": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            ),
            "cotton": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            ),
            "soybean": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            ),
            "wheat": AssetDefinition.create(
                title=None, description=None, media_type=MediaType.COG, roles=["data"]
            ),
        },
        "classes": [
            {
                "value": 1,
                "description": "Planted 1 time in 14 years",
                "color-hint": "F5F5DB",
            },
            {
                "value": 2,
                "description": "Planted 2 time in 14 years",
                "color-hint": "FFFF00",
            },
            {
                "value": 3,
                "description": "Planted 3 time in 14 years",
                "color-hint": "FFD200",
            },
            {
                "value": 4,
                "description": "Planted 4 time in 14 years ",
                "color-hint": "FFA600",
            },
            {
                "value": 5,
                "description": "Planted 5 time in 14 years",
                "color-hint": "9F522C",
            },
            {
                "value": 6,
                "description": "Planted 6 time in 14 years",
                "color-hint": "A62929",
            },
            {
                "value": 7,
                "description": "Planted 7 time in 14 years",
                "color-hint": "FF0000",
            },
            {
                "value": 8,
                "description": "Planted 8 time in 14 years",
                "color-hint": "DF1378",
            },
            {
                "value": 9,
                "description": "Planted 9 time in 14 years",
                "color-hint": "AC2C92",
            },
            {
                "value": 10,
                "description": "Planted 10 time in 14 years",
                "color-hint": "9F1FEC",
            },
            {
                "value": 11,
                "description": "SPlanted 11 time in 14 years",
                "color-hint": "6600EC",
            },
            {
                "value": 12,
                "description": "Planted 12 time in 14 years",
                "color-hint": "4D00FF",
            },
            {
                "value": 13,
                "description": "Planted 13 time in 14 years",
                "color-hint": "0000FF",
            },
            {
                "value": 14,
                "description": "Planted 14 time in 14 years",
                "color-hint": "0000B7",
            },
        ],
    },
}
