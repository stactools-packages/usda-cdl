# stactools-usda-cdl

[![PyPI](https://img.shields.io/pypi/v/stactools-usda-cdl)](https://pypi.org/project/stactools-usda-cdl/)

- Name: usda-cdl
- Package: `stactools.usda_cdl`
- PyPI: https://pypi.org/project/stactools-usda-cdl/
- Owner: @pholleway
- Dataset homepage: https://www.nass.usda.gov/Research_and_Science/Cropland/Release/index.php
- STAC extensions used:
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection/)

A stactools package for USDA Cropland Data Layer (CDL) product. 

The USDA Cropland Data Layer (CDL) is a crop-specific land cover data layer. The data is provided at 30 m resolution over the Contiguous United States(CONUS) from 2008 to Present. The USDA CDL is produced using satellite imagery from the Landsat 8 OLI/TIRS sensor, the ISRO ResourceSat-2 LISS-3, and the ESA SENTINEL-2 sensors collected during the current growing season.

This package can generate STAC files from TIFF files that link to the Cloud-Optimized GeoTiff (COG) files.

## Installation
```shell
pip install stactools-usda-cdl
```
## Examples

There is an example Catalog at examples/catalog.json. 

## Command-line Usage

Use `stac usda-cdl --help` to see all subcommands and options.

### Collection

Create a collection:

```shell
stac usda-cdl create-collection collection.json
```

Get information about all options for collection creation:

```shell
stac usda-cdl create-collection --help
```

### Item

Create a cropland item:

```shell
stac usda-cdl create-cropland-item /path/to/source/file.tif item.json --collection collection.json
```

Get information about all options for item creation:

```shell
stac usda-cdl create-cropland-item --help
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
