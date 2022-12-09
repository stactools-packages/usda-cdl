# import glob
import os.path
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

    def test_create_cropland_item_command(self) -> None:
        infile = test_data.get_path("data-files/basic_cropland_2020.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-cropland-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir, "basic_cropland_2020.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_cultivated_item_command(self) -> None:
        infile = test_data.get_path("data-files/ancillary_cultivated_2021.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-cultivated-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir, "ancillary_cultivated_2021.json")
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_frequency_item_command(self) -> None:
        corn_infile = test_data.get_path("data-files/frequency_corn_2021.tif")
        cotton_infile = test_data.get_path("data-files/frequency_cotton_2021.tif")
        soybean_infile = test_data.get_path("data-files/frequency_soybean_2021.tif")
        wheat_infile = test_data.get_path("data-files/frequency_wheat_2021.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-frequency-item {corn_infile} {cotton_infile} {soybean_infile} {wheat_infile} {tmp_dir}"  # noqa
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir, "frequency_corn_2021.json")
            item = pystac.read_file(item_path)
        item.validate()
