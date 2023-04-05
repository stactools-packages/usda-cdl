import os
import pathlib
from typing import List

import requests
from tqdm import tqdm

from stactools.usda_cdl.constants import FIRST_AVAILABLE_YEAR, MOST_RECENT_YEAR


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
        urls.append(
            "https://www.nass.usda.gov/Research_and_Science/Cropland"
            f"/Release/datasets/{year}_30m_cdls.zip"
        )
        # in 2017 and beyond there is a confidence layer available
        if year >= 2017:
            confidence_url = (
                "https://www.nass.usda.gov/Research_and_Science/Cropland"
                f"/Release/datasets/{year}_30m_confidence_layer.zip"
            )
            # in 2021 they changed the file basename slightly ¯\_(ツ)_/¯
            if year >= 2021:
                confidence_url = confidence_url.replace("layer", "Layer")

            urls.append(confidence_url)

        # each year, a new version of the cumalative (2008-present) "Cultivated"
        # and "Crop Frequency" layers are generated
        if year == MOST_RECENT_YEAR:
            urls.append(
                "https://www.nass.usda.gov/Research_and_Science/Cropland"
                f"/Release/datasets/{MOST_RECENT_YEAR}_Cultivated_Layer.zip"
            )
            urls.append(
                "https://www.nass.usda.gov/Research_and_Science/Cropland"
                "/Release/datasets/Crop_Frequency_"
                f"{FIRST_AVAILABLE_YEAR}-{MOST_RECENT_YEAR}.zip"
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
