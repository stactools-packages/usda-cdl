"""Tile and create STAC metadata for the USDA Cropland Data Layer (CDL)."""

from stactools.cli.registry import Registry


def register_plugin(registry: Registry) -> None:
    """Registers this click subcommand with the top-level `stac` CLI interface."""

    from stactools.usda_cdl import commands

    registry.register_subcommand(commands.create_usda_cdl_command)


__version__ = "0.1.0"
