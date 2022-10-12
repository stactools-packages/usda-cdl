from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict

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


class Frequency(str, Enum):  # update to collection
    base = "base"
    ancillary = "ancillary"


class Variable(str, Enum):
    Cropland = "cropland"
    Confidence = "confidence"
    Cultivated = "cultivated"
    Corn = "corn"
    Cotton = "cotton"
    Soybean = "soybean"
    Wheat = "wheat"


class CollectionType(str, Enum):
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
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Confidence: [
        {
            "data_type": "uint8",
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Cultivated: [
        {
            "data_type": "uint8",
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Corn: [
        {
            "data_type": "uint8",
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Cotton: [
        {
            "data_type": "uint8",
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Soybean: [
        {
            "data_type": "uint8",
            "nodata": "nan",
            "spatial_resolution": 30,
        }
    ],
    Variable.Wheat: [
        {
            "data_type": "uint8",
            "nodata": "nan",
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
    },
}
