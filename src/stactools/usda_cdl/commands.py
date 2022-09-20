import logging
import os
from tempfile import TemporaryDirectory
from typing import List

import click
from click import Command, Group
from pystac import CatalogType, Item
from stactools.core.copy import move_asset_file_to_item

from stactools.usda_cdl import stac
from stactools.usda_cdl.constants import Variable
from stactools.usda_cdl.utils import data_frequency

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
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    def create_collection_command(infile: str, outdir: str) -> None:
        """Creates a STAC Collection with Items generated from the HREFs listed
        in INFILE. COGs are also generated and stored alongside the Items.

        The INFILE should contain only cdl or only cdl-ancillary HREFs. Only a
        single HREF to a single variable (prcp, tavg, tmax, or tmin) should be
        listed in the INFILE.

        \b
        Args:
            infile (str): Text file containing one HREF to a TIFF file per
                line.
            outdir (str): Directory that will contain the collection.

        """
        with open(infile) as f:
            hrefs = [os.path.abspath(line.strip()) for line in f.readlines()]

        items: List[Item] = []
        frequency = data_frequency(hrefs[0])
        with TemporaryDirectory():
            for href in hrefs:
                temp_items, _ = stac.create_items(href)
                items.extend(temp_items)

            collection = stac.create_collection(frequency)
            collection.catalog_type = CatalogType.SELF_CONTAINED
            collection.set_self_href(
                os.path.join(outdir, f"{frequency}/collection.json")
            )

            collection.add_items(items)
            collection.update_extent_from_items()

            # Only move the COGs (not the source netCDFs) next to the Items
            for item in collection.get_all_items():
                for var in Variable:
                    new_href = move_asset_file_to_item(
                        item, item.assets[var].href, ignore_conflicts=True
                    )
                    item.assets[var].href = new_href

            collection.make_all_asset_hrefs_relative()

        collection.validate_all()
        collection.save()

        return None

    @usda_cdl.command("create-items", short_help="Creates STAC Items")
    @click.argument("INFILE")
    @click.option(
        "-c",
        "--cog-check-href",
        type=str,
        help="HREF to directory to check for existing COGs",
    )
    def create_items_command(infile: str) -> None:
        """Creates COGs and STAC Items for each day or month in the daily or
        monthly netCDF INFILE.

        \b
        Args:
            infile (str): HREF to a TIFF file for one of the four variables:
                prcp, tavg, tmax, and tmin. The netCDF files for the remaining
                three variable must exist alongside `infile`.
            cogdir (str): Directory that will contain the COGs.
            itemdir (str): Directory that will contain the STAC Items.
        """
        items, _ = stac.create_items(
            infile,
        )
        for item in items:
            item_path = os.path.join(f"{item.id}.json")
            item.set_self_href(item_path)
            item.make_asset_hrefs_relative()
            item.validate()
            item.save_object(include_self_link=False)

        return None

    return usda_cdl
