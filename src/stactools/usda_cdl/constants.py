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
        "classes": [{
            "value": 1,
            "description": "Tree cover",
            "color-hint": "006400"
        }, {
            "value": 2,
            "description": "Shrubland",
            "color-hint": "FFBB22"
        }]
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
        "classes": [{
            "value": 1,
            "description": "Non-Cultivated",
            "color-hint": "000000"
        }, {
            "value": 2,
            "description": "Cultivated",
            "color-hint": "006300"
        }]
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
        "classes": [{
            "value": 1,
            "description": "Planted 1 time in 14 years",
            "color-hint": "F5F5DB"
        }, {
            "value": 2,
            "description": "Planted 2 time in 14 years",
            "color-hint": "FFFF00"
        },{
            "value": 3,
            "description": "Planted 3 time in 14 years",
            "color-hint": "FFD200"
        },{
            "value": 4,
            "description": "Planted 4 time in 14 years ",
            "color-hint": "FFA600"
        },{
            "value": 5,
            "description": "Planted 5 time in 14 years",
            "color-hint": "9F522C"
        },{
            "value": 6,
            "description": "Planted 6 time in 14 years",
            "color-hint": "A62929"
        },{
            "value": 7,
            "description": "Planted 7 time in 14 years",
            "color-hint": "FF0000"
        },{
            "value": 8,
            "description": "Planted 8 time in 14 years",
            "color-hint": "DF1378"
        },{
            "value": 9,
            "description": "Planted 9 time in 14 years",
            "color-hint": "AC2C92"
        },{
            "value": 10,
            "description": "Planted 10 time in 14 years",
            "color-hint": "9F1FEC"
        },{
            "value": 11,
            "description": "SPlanted 11 time in 14 years",
            "color-hint": "6600EC"
        },{
            "value": 12,
            "description": "Planted 12 time in 14 years",
            "color-hint": "4D00FF"
        },{
            "value": 13,
            "description": "Planted 13 time in 14 years",
            "color-hint": "0000FF"
        },{
            "value": 14,
            "description": "Planted 14 time in 14 years",
            "color-hint": "0000B7"
        }]
    }
}
