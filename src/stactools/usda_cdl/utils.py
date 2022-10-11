import os
from typing import Any, Dict

from pystac import MediaType

from stactools.usda_cdl import constants
from stactools.usda_cdl.constants import Frequency, Variable


def data_frequency(href: str) -> Frequency:
    """Determine if data collection is 'usda_cdl' or 'usda_cdl_ancillary' from the passed HREF.

    Args:
        href (str): HREF to a COG file.

    Returns:
        Collection: Enum of 'cdl' or 'cdl_ancillary'.
    """
    basename = os.path.splitext(os.path.basename(href))[0]
    frequency = (
        Frequency.USDA_CDL
        if basename.startswith("usda_cdl")
        else Frequency.USDA_CDL_ANCILLARY
    )
    return frequency


def cog_asset_dict(frequency: Frequency, var: Variable) -> Dict[str, Any]:
    """Returns a COG asset, less the HREF, in dictionary form.

    Args:
        var (Variable):  One of 'prcp', 'tavg', 'tmax', or 'tmin'.

    Returns:
        Dict[str, Any]: A partial dictionary of STAC Asset components.
    """
    return {
        "type": MediaType.COG,
        "roles": constants.COG_ROLES,
        "title": f"{frequency.capitalize()} {constants.COG_ASSET_TITLES[var]}",
        "raster:bands": constants.COG_RASTER_BANDS[var],
    }
