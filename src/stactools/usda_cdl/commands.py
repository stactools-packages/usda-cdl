import logging
import os

import click
from click import Command, Group

from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import CollectionType

logger = logging.getLogger(__name__)


def create_usda_cdl_command(cli: Group) -> Command:
    """Creates the stactools-usda-cdl command line utility."""

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
    @click.argument("COLLECTION_TYPE")
    @click.argument("OUTFILE")
    def create_collection_command(collection_type: str, outfile: str) -> None:
        """
        Creates a STAC Collection with Items generated from the HREFs listed
        in INFILE. COGs are also generated and stored alongside the Items.

        The INFILE should contain only cropland, cultivated, or frequency HREFs.
        Only a single HREF to a single variable should be listed in the INFILE.

        Args:
            infile (str): Text file containing one HREF to a TIFF file per line.
            outfile (str): The filename of the output collection.
        """
        collection_type = CollectionType.from_str(collection_type)
        collection = stac.create_collection(collection_type)
        collection.set_self_href(outfile)
        collection.validate_all()
        collection.save()

    @usda_cdl.command("create-cropland-item", short_help="Creates STAC Cropland Items")
    @click.argument("INFILE")  # how to handle option file?
    @click.argument("OUTDIR")
    def create__cropland_item_command(infile: str, outdir: str) -> None:
        """
        Creates a STAC Item.

        Args:
            infile (str): HREF of the cropland COG.
            outdir (str): Directory that will contain the STAC Item.
        """
        item = stac.create_cropland_item(infile)
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    @usda_cdl.command(
        "create-cultivated-item", short_help="Creates STAC Cultivated Items"
    )
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    def create__cultivated_item_command(infile: str, outdir: str) -> None:
        """
        Creates a STAC Item.

        Args:
                infile (str): HREF of the cultivated COG.
                outdir (str): Directory that will contain the STAC Item.
        """
        item = stac.create_cultivated_item(infile)
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    @usda_cdl.command(
        "create-frequency-item", short_help="Creates STAC Frequnecy Items"
    )
    @click.argument("CORN_INFILE")
    @click.argument("COTTON_INFILE")
    @click.argument("SOYBEAN_INFILE")
    @click.argument("WHEAT_INFILE")
    @click.argument("OUTDIR")
    def create__frequency_item_command(
        corn_infile: str,
        cotton_infile: str,
        soybean_infile: str,
        wheat_infile: str,
        outdir: str,
    ) -> None:
        """
        Creates a STAC Item.

        Args:
                corn_infile (str): HREF of the corn frequency COG.
                cotton_infile (str): HREF of the cotton frequency COG.
                soybean_infile (str): HREF of the soybean frequency COG.
                wheat_infile (str): HREF of the wheat frequency COG.
                outdir (str): Directory that will contain the STAC Item.
        """
        item = stac.create_frequency_item(
            corn_infile, cotton_infile, soybean_infile, wheat_infile
        )
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    return usda_cdl
