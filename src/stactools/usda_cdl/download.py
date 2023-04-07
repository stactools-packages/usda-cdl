import os
import pathlib
from typing import List

import requests
from tqdm import tqdm

from stactools.usda_cdl.constants import FIRST_AVAILABLE_YEAR, MOST_RECENT_YEAR

URL_BASE = "https://www.nass.usda.gov/Research_and_Science/Cropland/Release/datasets/"

CROPLAND_URL = URL_BASE + "{year}_30m_cdls.zip"
CONFIDENCE_URL = URL_BASE + "{year}_30m_confidence_layer.zip"
FREQUENCY_URL = URL_BASE + "Crop_Frequency_{first_year}-{last_year}.zip"
CULTIVATED_URL = URL_BASE + "{year}_Cultivated_Layer.zip"


def download_zips(years: List[int], destination: pathlib.Path) -> List[pathlib.Path]:
    """Download zipped GeoTiffs from USDA

    Args:
        years: list of years to download
        destination: destination directory for downloaded files

    Returns: list of filepaths for downloaded zip files
    """
    os.makedirs(str(destination), exist_ok=True)
    if not years:
        years = list(range(FIRST_AVAILABLE_YEAR, MOST_RECENT_YEAR + 1))
    urls = list()
    for year in years:
        if year < FIRST_AVAILABLE_YEAR or year > MOST_RECENT_YEAR:
            raise Exception(f"Unsupported CDL year: {year}")
        urls.append(CROPLAND_URL.format(year=year))

        # in 2017 and beyond there is a confidence layer available
        if year >= 2017:
            confidence_url = CONFIDENCE_URL.format(year=year)
            # in 2021 they changed the file basename slightly ¯\_(ツ)_/¯
            if year >= 2021:
                confidence_url = confidence_url.replace(
                    "confidence_layer", "Confidence_Layer"
                )

            urls.append(confidence_url)

        # starting in 2020, the "Cultivated" and cumalative (2008-present)
        # "Crop Frequency" layers are available
        if year >= 2020:
            urls.append(CULTIVATED_URL.format(year=year))
            urls.append(
                FREQUENCY_URL.format(first_year=FIRST_AVAILABLE_YEAR, last_year=year)
            )

    zips = []
    for url in urls:
        path = pathlib.Path(str(destination)) / os.path.basename(url)
        if path.exists():
            print(f"{path} already exists, skipping...")
            continue
        response = requests.get(url, stream=True)
        with tqdm.wrapattr(
            open(path, "wb"),
            "write",
            miniters=1,
            desc=url.split("/")[-1],
            total=int(response.headers.get("content-length", 0)),
        ) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)

        zips.append(path)

    return zips
