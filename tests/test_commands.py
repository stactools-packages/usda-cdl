import glob
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.usda_cdl.commands import create_usda_cdl_command
from tests import test_data


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_usda_cdl_command]

    def test_create_usda_cdl_items(self) -> None:
        nc_href = test_data.get_path("data-files/netcdf/monthly/nclimgrid_prcp.nc")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-items {nc_href} {tmp_dir} {tmp_dir}"
            self.run_command(cmd)

            cog_files = glob.glob(f"{tmp_dir}/*tif")
            assert len(cog_files) == 8
            item_files = glob.glob(f"{tmp_dir}/*.json")
            assert len(item_files) == 2

            for item_file in item_files:
                item = pystac.read_file(item_file)
                item.validate()

    def test_create_usda_cdl_ancillary_items(self) -> None:
        nc_href = test_data.get_path(
            "data-files/netcdf/daily/beta/by-month/2022/01/prcp-202201-grd-prelim.nc"
        )
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-items {nc_href} {tmp_dir} {tmp_dir}"
            self.run_command(cmd)

            cog_files = glob.glob(f"{tmp_dir}/*tif")
            assert len(cog_files) == 4
            item_files = glob.glob(f"{tmp_dir}/*.json")
            assert len(item_files) == 1

            for item_file in item_files:
                item = pystac.read_file(item_file)
                item.validate()

    def test_create_monthly_collection(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            file_list_path = f"{tmp_dir}/test_monthly.txt"
            with open(file_list_path, "w") as f:
                f.write(
                    test_data.get_path("data-files/netcdf/monthly/nclimgrid_prcp.nc")
                )

            cmd = f"usda-cdl create-collection {file_list_path} {tmp_dir}"
            self.run_command(cmd)

            item_paths = ["monthly/nclimgrid-189501", "monthly/nclimgrid-189502"]
            for item_path in item_paths:
                item_files = glob.glob(f"{tmp_dir}/{item_path}/*.json")
                assert len(item_files) == 1
                cog_files = glob.glob(f"{tmp_dir}/{item_path}/*.tif")
                assert len(cog_files) == 4

            collection = pystac.read_file(f"{tmp_dir}/monthly/collection.json")
            collection.validate()
