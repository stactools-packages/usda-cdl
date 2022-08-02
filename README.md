# stactools-cdl

[![PyPI](https://img.shields.io/pypi/v/stactools-cdl)](https://pypi.org/project/stactools-cdl/)

- Name: cdl
- Package: `stactools.cdl`
- PyPI: https://pypi.org/project/stactools-cdl/
- Owner: @pholleway
- Dataset homepage: http://example.com
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `cdl:custom`: A custom attribute

The stactools-cdl package generates STAC Items and Collections for the USDA Cropland Data Layer. 

## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation
```shell
pip install stactools-cdl
```

## Command-line Usage

Description of the command line functions

```shell
$ stac cdl create-item source destination
```

Use `stac cdl --help` to see all subcommands and options.

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
