import stactools.core
from stactools.cli.registry import Registry

from stactools.usda_cdl.stac import (
    create_cropland_item,
    create_cultivated_item,
    create_frequency_item,
)

__all__ = [
    "create_cropland_item",
    "create_cultivated_item",
    "create_frequency_item",
    "create_collection",
]

stactools.core.use_fsspec()


def register_plugin(registry: Registry) -> None:
    from stactools.usda_cdl import commands

    registry.register_subcommand(commands.create_usda_cdl_command)


__version__ = "0.1.0"
