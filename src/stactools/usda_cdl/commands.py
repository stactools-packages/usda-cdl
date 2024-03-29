import logging
import os
import pathlib
from typing import List

import click
from click import Command, Group, Path

from stactools.usda_cdl import stac, tile
from stactools.usda_cdl.download import download_zips
from stactools.usda_cdl.tile import DEFAULT_WINDOW_SIZE

logger = logging.getLogger(__name__)


def create_usda_cdl_command(cli: Group) -> Command:
    """Creates the `stac usda-cdl` subcommand."""

    @cli.group(
        "usda-cdl",
        short_help=("Commands for working with stactools-usda-cdl"),
    )
    def usda_cdl() -> None:
        pass

    @usda_cdl.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("OUTFILE")
    def create_collection_command(outfile: str) -> None:
        """
        Creates a STAC Collection.

        Args:
            outfile (str): The filename of the output collection.
        """
        collection = stac.create_collection()
        collection.set_self_href(outfile)
        collection.validate()
        collection.save()

    @usda_cdl.command("create-item", short_help="Creates a STAC item")
    @click.argument("HREFS", nargs=-1)
    @click.argument("OUTFILE", nargs=1)
    def create_item_command(hrefs: List[str], outfile: str) -> None:
        """
        Creates a STAC Item from the provided hrefs.

        This will error if the time interval or geometries of the assets are not
        the same.

        Args:
            hrefs (str): HREFs to COGs.
            outfile (str): The output file.
        """
        item = stac.create_item_from_hrefs(hrefs)
        item.set_self_href(outfile)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object(include_self_link=False)

    @usda_cdl.command("tile", short_help="Tile a geotiff (zipped or not zipped)")
    @click.argument("infile")
    @click.argument("destination")
    @click.option(
        "-s",
        "--size",
        help="Size, in pixels, of each tile",
        default=DEFAULT_WINDOW_SIZE,
        show_default=True,
    )
    def tile_file(infile: Path, destination: Path, size: int) -> None:
        """Tiles the input file, placing the tiles in the destination directory."""
        os.makedirs(str(destination), exist_ok=True)
        infile_as_path = pathlib.Path(str(infile))
        if infile_as_path.suffix == ".zip":
            tile.tile_zipfile(infile_as_path, pathlib.Path(str(destination)), size)
        else:
            tile.tile_geotiff(infile_as_path, pathlib.Path(str(destination)), size)

    @usda_cdl.command("download", short_help="Download zipped source GeoTIFFs")
    @click.argument("years", nargs=-1, type=int)
    @click.argument("destination", nargs=1)
    def download(years: List[int], destination: Path) -> None:
        """Downloads the USDA CDL zip files to the destination directory. It's a
        lot of data, so this will take a while.

        If you just want to download specific years' data, provide those years
        on the command line before the destination directory.
        """
        download_zips(years, pathlib.Path(str(destination)))

    return usda_cdl
