from datetime import datetime
from typing import Any, Dict

from pystac import Extent, Link, Provider, ProviderRole, SpatialExtent, TemporalExtent
from pystac.extensions.item_assets import AssetDefinition

CLASSIFICATION_SCHEMA = (
    "https://stac-extensions.github.io/classification/v1.1.0/schema.json"
)

# Collection
COLLECTION_ID = "cdl"
COLLECTION_TITLE = "USDA Cropland Data Layer"
COLLECTION_DESCRIPTION = "The CDL is a crop-specific land cover classification product of more than 100 crop categories grown in the United States. CDLs are derived using a supervised land cover classification of satellite imagery. The supervised classification relies on first manually identifying pixels within certain images, often called training sites, which represent the same crop or land cover type. Using these training sites, a spectral signature is developed for each crop type that is then used by the analysis software to identify all other pixels in the satellite image representing the same crop. Using this method, a new CDL is compiled annually and released to the public a few months after the end of the growing season."  # noqa
PROVIDERS = [
    Provider(
        name="USDA-NASS",
        roles=[ProviderRole.PRODUCER, ProviderRole.LICENSOR],
        description="United States Department of Agriculture - National Agricultural Statistics Service",  # noqa
        url="https://www.nass.usda.gov/",
    ),
]
LINK_LANDING_PAGE = Link(
    target="https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php",
    media_type="text/html",
    title="Product Landing Page",
    rel="about",
)
KEYWORDS = ["Land Cover", "Land Use", "USDA", "Agriculture"]

# Items
ITEM_DESCRIPTION = {
    "Cropland": "USDA National Cropland Data Layer (CDL) at 30 meter resolution over CONUS.",
    "Cultivated": "USDA National Cultivated Layer at 30 meter resolution over CONUS. The Cultivated Layer is based on the most recent five years.",  # noqa
    "Frequency": "USDA National Frequency Layer for corn, cotton, soybeans, and wheat at 30 meter resolution over CONUS. The Frequency Layer identifies crop specific planting frequency and are based on land cover information derived from the CDLs.",  # noqa
    "Condfidence": "USDA National Confidence Layer at 30 meter resolution over CONUS.",
    # data layers to add later
}

# Assets
ASSET_PROPS: Dict[str, Any] = {
    "title": "CDL",
    "description": "USDA Cropland Data Classifications",  # noqa
    "type": "image/tiff; application=geotiff; profile=cloud-optimized",
    "roles": ["data"],
    "raster:bands": [
        {
            "description": "Classifications",
            "sampling": "area",
            "data_type": "uint8",
            "unit": "meter",
        }
    ],
    "classification:classes": [
        {"value": 0, "description": "Background", "color_hint": "FF0000"},
        {"value": 1, "description": "Corn", "color_hint": "FF0000"},
        {"value": 2, "description": "Cotton", "color_hint": "FF0000"},
        {"value": 3, "description": "Rice", "color_hint": "FF0000"},
        {"value": 4, "description": "Sorghum", "color_hint": "FF0000"},
        {"value": 5, "description": "Soybeans", "color_hint": "FF0000"},
        {"value": 6, "description": "Sunflower", "color_hint": "FF0000"},
        {"value": 10, "description": "Peanuts", "color_hint": "FF0000"},
        {"value": 11, "description": "Tobacco", "color_hint": "FF0000"},
        {"value": 12, "description": "Sweet Corn", "color_hint": "FF0000"},
        {"value": 13, "description": "Pop or Orn Corn", "color_hint": "FF0000"},
        {"value": 14, "description": "Mint", "color_hint": "FF0000"},
        {"value": 21, "description": "Barley", "color_hint": "FF0000"},
        {"value": 22, "description": "Durum Wheat", "color_hint": "FF0000"},
        {"value": 23, "description": "Spring Wheat", "color_hint": "FF0000"},
        {"value": 24, "description": "Winter Wheat", "color_hint": "FF0000"},
        {"value": 25, "description": "Other Small Grains", "color_hint": "FF0000"},
        {
            "value": 26,
            "description": "Dbl Crop Winter Wheat/Soybeans",
            "color_hint": "FF0000",
        },
        {"value": 27, "description": "Rye", "color_hint": "FF0000"},
        {"value": 28, "description": "Oats", "color_hint": "FF0000"},
        {"value": 29, "description": "Millet", "color_hint": "FF0000"},
        {"value": 30, "description": "Speltz", "color_hint": "FF0000"},
        {"value": 31, "description": "Canola", "color_hint": "FF0000"},
        {"value": 32, "description": "Flaxseed", "color_hint": "FF0000"},
        {"value": 33, "description": "Safflower", "color_hint": "FF0000"},
        {"value": 34, "description": "Rape Seed", "color_hint": "FF0000"},
        {"value": 35, "description": "Mustard", "color_hint": "FF0000"},
        {"value": 36, "description": "Alfalfa", "color_hint": "FF0000"},
        {"value": 37, "description": "Other Hay/Non Alfalfa", "color_hint": "FF0000"},
        {"value": 38, "description": "Camelina", "color_hint": "FF0000"},
        {"value": 39, "description": "Buckwheat", "color_hint": "FF0000"},
        {"value": 41, "description": "Sugarbeets", "color_hint": "FF0000"},
        {"value": 42, "description": "Dry Beans", "color_hint": "FF0000"},
        {"value": 43, "description": "Potatoes", "color_hint": "FF0000"},
        {"value": 44, "description": "Other Crops", "color_hint": "FF0000"},
        {"value": 45, "description": "Sugarcane", "color_hint": "FF0000"},
        {"value": 46, "description": "Sweet Potatoes", "color_hint": "FF0000"},
        {"value": 47, "description": "Misc. Vegs & Fruits", "color_hint": "FF0000"},
        {"value": 48, "description": "Watermelons", "color_hint": "FF0000"},
        {"value": 49, "description": "Onions", "color_hint": "FF0000"},
        {"value": 50, "description": "Cucumbers", "color_hint": "FF0000"},
        {"value": 51, "description": "Chick Peas", "color_hint": "FF0000"},
        {"value": 52, "description": "Lentils", "color_hint": "FF0000"},
        {"value": 53, "description": "Peas", "color_hint": "FF0000"},
        {"value": 54, "description": "Tomatoes", "color_hint": "FF0000"},
        {"value": 55, "description": "Caneberries", "color_hint": "FF0000"},
        {"value": 56, "description": "Hops", "color_hint": "FF0000"},
        {"value": 57, "description": "Herbs", "color_hint": "FF0000"},
        {"value": 58, "description": "Clover/Wildflowers", "color_hint": "FF0000"},
        {"value": 59, "description": "Sod/Grass Seed", "color_hint": "FF0000"},
        {"value": 60, "description": "Switchgrass", "color_hint": "FF0000"},
        {"value": 61, "description": "Idle Cropland", "color_hint": "FF0000"},
        {"value": 63, "description": "Forest", "color_hint": "FF0000"},
        {"value": 64, "description": "Shrubland", "color_hint": "FF0000"},
        {"value": 65, "description": "Barren", "color_hint": "FF0000"},
        {"value": 66, "description": "Cherries", "color_hint": "FF0000"},
        {"value": 67, "description": "Peaches", "color_hint": "FF0000"},
        {"value": 68, "description": "Apples", "color_hint": "FF0000"},
        {"value": 69, "description": "Grapes", "color_hint": "FF0000"},
        {"value": 70, "description": "Christmas Trees", "color_hint": "FF0000"},
        {"value": 71, "description": "Other Tree Crops", "color_hint": "FF0000"},
        {"value": 72, "description": "Citrus", "color_hint": "FF0000"},
        {"value": 74, "description": "Pecans", "color_hint": "FF0000"},
        {"value": 75, "description": "Almonds", "color_hint": "FF0000"},
        {"value": 76, "description": "Walnuts", "color_hint": "FF0000"},
        {"value": 77, "description": "Pears", "color_hint": "FF0000"},
        {"value": 81, "description": "Clouds/No Data", "color_hint": "FF0000"},
        {"value": 82, "description": "Developed", "color_hint": "FF0000"},
        {"value": 83, "description": "Water", "color_hint": "FF0000"},
        {"value": 87, "description": "Wetlands", "color_hint": "FF0000"},
        {"value": 88, "description": "Nonag/Undefined", "color_hint": "FF0000"},
        {"value": 92, "description": "Aquaculture", "color_hint": "FF0000"},
        {"value": 111, "description": "Open Water", "color_hint": "FF0000"},
        {"value": 112, "description": "Perennial Ice/Snow", "color_hint": "FF0000"},
        {"value": 121, "description": "Developed/Open Space", "color_hint": "FF0000"},
        {
            "value": 122,
            "description": "Developed/Low Intensity",
            "color_hint": "FF0000",
        },
        {
            "value": 123,
            "description": "Developed/Med Intensity",
            "color_hint": "FF0000",
        },
        {
            "value": 124,
            "description": "Developed/High Intensity",
            "color_hint": "FF0000",
        },
        {"value": 131, "description": "Barren", "color_hint": "FF0000"},
        {"value": 141, "description": "Deciduous Forest", "color_hint": "FF0000"},
        {"value": 142, "description": "Evergreen Forest", "color_hint": "FF0000"},
        {"value": 143, "description": "Mixed Forest", "color_hint": "FF0000"},
        {"value": 152, "description": "Shrubland", "color_hint": "FF0000"},
        {"value": 176, "description": "Grassland/Pasture", "color_hint": "FF0000"},
        {"value": 190, "description": "Woody Wetlands", "color_hint": "FF0000"},
        {"value": 195, "description": "Herbaceous Wetlands", "color_hint": "FF0000"},
        {"value": 204, "description": "Pistachios", "color_hint": "FF0000"},
        {"value": 205, "description": "Triticale", "color_hint": "FF0000"},
        {"value": 206, "description": "Carrots", "color_hint": "FF0000"},
        {"value": 207, "description": "Asparagus", "color_hint": "FF0000"},
        {"value": 208, "description": "Garlic", "color_hint": "FF0000"},
        {"value": 209, "description": "Cantaloupes", "color_hint": "FF0000"},
        {"value": 210, "description": "Prunes", "color_hint": "FF0000"},
        {"value": 211, "description": "Olives", "color_hint": "FF0000"},
        {"value": 212, "description": "Oranges", "color_hint": "FF0000"},
        {"value": 213, "description": "Honeydew Melons", "color_hint": "FF0000"},
        {"value": 214, "description": "Broccoli", "color_hint": "FF0000"},
        {"value": 215, "description": "Avocados", "color_hint": "FF0000"},
        {"value": 216, "description": "Peppers", "color_hint": "FF0000"},
        {"value": 217, "description": "Pomegranates", "color_hint": "FF0000"},
        {"value": 218, "description": "Nectarines", "color_hint": "FF0000"},
        {"value": 219, "description": "Greens", "color_hint": "FF0000"},
        {"value": 220, "description": "Plums", "color_hint": "FF0000"},
        {"value": 221, "description": "Strawberries", "color_hint": "FF0000"},
        {"value": 222, "description": "Squash", "color_hint": "FF0000"},
        {"value": 223, "description": "Apricots", "color_hint": "FF0000"},
        {"value": 224, "description": "Vetch", "color_hint": "FF0000"},
        {
            "value": 225,
            "description": "Dbl Crop Winter Wheat/Corn",
            "color_hint": "FF0000",
        },
        {"value": 226, "description": "Dbl Crop Oats/Corn", "color_hint": "FF0000"},
        {"value": 227, "description": "Lettuce", "color_hint": "FF0000"},
        {
            "value": 228,
            "description": "Dbl Crop Triticale/Corn",
            "color_hint": "FF0000",
        },
        {"value": 229, "description": "Pumpkins", "color_hint": "FF0000"},
        {
            "value": 230,
            "description": "Dbl Crop Lettuce/Durum Wheat",
            "color_hint": "FF0000",
        },
        {
            "value": 231,
            "description": "Dbl Crop Lettuce/Cataloupe",
            "color_hint": "FF0000",
        },
        {
            "value": 232,
            "description": "Dbl Crop Lettuce/Cotton",
            "color_hint": "FF0000",
        },
        {
            "value": 233,
            "description": "Dbl Crop Lettuce/Barley",
            "color_hint": "FF0000",
        },
        {
            "value": 234,
            "description": "Dbl Crop Durum Wheat/Sorghum",
            "color_hint": "FF0000",
        },
        {
            "value": 235,
            "description": "Dbl Crop Barley/Sorghum",
            "color_hint": "FF0000",
        },
        {
            "value": 236,
            "description": "Dbl Crop Winter Wheat/Sorghum",
            "color_hint": "FF0000",
        },
        {"value": 237, "description": "Dbl Crop Barley/Corn", "color_hint": "FF0000"},
        {
            "value": 238,
            "description": "Dbl Crop Winter Wheat/Cotton",
            "color_hint": "FF0000",
        },
        {
            "value": 239,
            "description": "Dbl Crop Soybeans/Cotton",
            "color_hint": "FF0000",
        },
        {
            "value": 240,
            "description": "Dbl Crop Soybeans/Oats ",
            "color_hint": "FF0000",
        },
        {"value": 241, "description": "Dbl Crop Corn/Soybeans", "color_hint": "FF0000"},
        {"value": 242, "description": "Blueberries", "color_hint": "FF0000"},
        {"value": 243, "description": "Cabbage", "color_hint": "FF0000"},
        {"value": 244, "description": "Cauliflower", "color_hint": "FF0000"},
        {"value": 245, "description": "Celery", "color_hint": "FF0000"},
        {"value": 246, "description": "Radishes", "color_hint": "FF0000"},
        {"value": 247, "description": "Turnips", "color_hint": "FF0000"},
        {"value": 248, "description": "Eggplants", "color_hint": "FF0000"},
        {"value": 249, "description": "Gourds", "color_hint": "FF0000"},
        {"value": 250, "description": "Cranberries", "color_hint": "FF0000"},
        {
            "value": 254,
            "description": "Dbl Crop Barley/Soybeans",
            "color_hint": "FF0000",
        },
    ],
}
ITEM_ASSETS = {"data": AssetDefinition(ASSET_PROPS)}

# Metadata
RESOLUTION = 30
EXTENT = Extent(
    SpatialExtent(
        [
            [-129.16, 23.81, -65.69, 23.81],  # double check
        ]
    ),
    TemporalExtent([[datetime(2008, 1, 1), datetime(2021, 12, 31, 23, 59, 59)]]),
)
