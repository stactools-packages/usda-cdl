# stactools-usda-cdl

[![PyPI](https://img.shields.io/pypi/v/stactools-usda-cdl)](https://pypi.org/project/stactools-usda-cdl/)

- Name: usda-cdl
- Package: `stactools.usda_cdl`
- PyPI: https://pypi.org/project/stactools-usda-cdl/
- Owner: @pholleway
- Dataset homepage: http://example.com
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)

The stactools-usda-cdl package generates STAC Items and Collections for the USDA Cropland Data Layer (CDL). 

The USDA CDLs provides data for 2008 through 2021 in geodatabase form. This package assumes a raster has been extracted and tiled into smaller cloud optimized GeoTIFF (COG) image files. The tile filenames are expected to contain the prefix `USDA_CDL_{year}`.
## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation
```shell
pip install stactools-usda-cdl
```

## Command-line Usage

Description of the command line functions

```shell
$ stac usda-cdl create-item source destination
```

Use `stac usda-cdl --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
$ pip install -e .
$ pip install -r requirements-dev.txt
$ pre-commit install
```

To check all files:

```shell
$ pre-commit run --all-files
```

To run the tests:

```shell
$ pytest -vv
```
