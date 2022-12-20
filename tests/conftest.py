from pathlib import Path
from typing import List

import pytest

from . import test_data


@pytest.fixture
def cdl() -> Path:
    return Path(test_data.get_path("data-files/2021_30m_cdls.tif"))


@pytest.fixture
def cdl_tile() -> Path:
    return Path(
        test_data.get_path("data-files/tiles/2021_30m_cdls_-91095_1807575_15000.tif")
    )


@pytest.fixture
def confidence() -> Path:
    return Path(test_data.get_path("data-files/2021_30m_confidence_layer.tif"))


@pytest.fixture
def cultivated() -> Path:
    return Path(test_data.get_path("data-files/2021_cultivated_layer.tif"))


@pytest.fixture
def corn() -> Path:
    return Path(test_data.get_path("data-files/crop_frequency_corn_2008-2021.tif"))


@pytest.fixture
def cotton() -> Path:
    return Path(test_data.get_path("data-files/crop_frequency_cotton_2008-2021.tif"))


@pytest.fixture
def soybeans() -> Path:
    return Path(test_data.get_path("data-files/crop_frequency_soybeans_2008-2021.tif"))


@pytest.fixture
def wheat() -> Path:
    return Path(test_data.get_path("data-files/crop_frequency_wheat_2008-2021.tif"))


@pytest.fixture
def tiles() -> List[Path]:
    directory = test_data.get_path("data-files/tiles")
    return list(Path(directory).glob("*.tif"))
