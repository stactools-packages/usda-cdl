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

    def test_create_item_command(self) -> None:
        infile = test_data.get_path("data-files/2021_30m_cdls.tif")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"usda-cdl create-item {infile} {tmp_dir}/out.json"
            self.run_command(cmd)
            item_path = os.path.join(tmp_dir, "out.json")
            item = pystac.read_file(item_path)
            item.validate()
