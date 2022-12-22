# stactools-usda-cdl

[![PyPI](https://img.shields.io/pypi/v/stactools-usda-cdl)](https://pypi.org/project/stactools-usda-cdl/)

- Name: usda-cdl
- Package: `stactools.usda_cdl`
- PyPI: <https://pypi.org/project/stactools-usda-cdl/>
- Owner: @gadomski, @pholleway
- Dataset homepage: <https://www.nass.usda.gov/Research_and_Science/Cropland/Release/index.php>
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection/)
  - [raster](https://github.com/stac-extensions/raster/)
- Extra fields:
  - `usda_cdl:type`: The [item type](#item-types).
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/usda-cdl/main/examples/collection.json)

A stactools package for USDA Cropland Data Layer (CDL) product.

The USDA Cropland Data Layer (CDL) is a crop-specific land cover data layer. The data is provided at 30 m resolution over the Contiguous United States (CONUS) from 2008 to Present. The USDA CDL is produced using satellite imagery from the Landsat 8 OLI/TIRS sensor, the ISRO ResourceSat-2 LISS-3, and the ESA SENTINEL-2 sensors collected during the current growing season.

This package can generate STAC files from TIFF files that link to the Cloud-Optimized GeoTiff (COG) files.

## Item types

There are three primary item types in this dataset:

- `cropland`: Yearly crop-cover classification dataset, optionally with a confidence product.
- `cultivated`: A boolean raster describing whether a given pixel was "cultivated" in the target year.
- `frequency`: A set of four rasters that describe how often four main crop types were planted in the past fourteen years.

## Examples

There is an example collection at examples/collection.json.

### Tiling

While this stactools package can create items for the original, CONUS-wide GeoTIFFS, it also supports tiling the data into more manageable sized Cloud-Optimized GeoTIFFs.
To tile a GeoTIFF:

```shell
stac usda-cdl tile --size 500 tests/data-files/2021_30m_cdls.tif tiles
```

If you have a bunch of hrefs to existing tiles, you can use `stac.create_items_from_tiles` to intelligantly partition those hrefs by product type and tile:

```python
from stactools.usda_cdl import stac
from pathlib import Path
hrefs = list(Path("tests/data-files/tiles").glob("*.tif"))
items = stac.create_items_from_tiles(hrefs)
```

## Installation

```shell
pip install stactools-usda-cdl
```

## Command-line Usage

Use `stac usda-cdl --help` to see all subcommands and options.

### Collection

Create a collection:

```shell
stac usda-cdl create-collection collection.json
```

### Item

Create an item:

```shell
stac usda-cdl create-item /path/to/source/file.tif item.json
```

Get information about all options for item creation:

```shell
stac usda-cdl create-item --help
```

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```
