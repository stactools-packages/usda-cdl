from stactools.cli.registry import Registry


def register_plugin(registry: Registry) -> None:
    from stactools.usda_cdl import commands

    registry.register_subcommand(commands.create_usda_cdl_command)


__version__ = "0.1.0"
