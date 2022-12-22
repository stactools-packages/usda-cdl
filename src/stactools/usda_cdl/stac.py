from collections import defaultdict
from typing import DefaultDict, List, Optional

import stactools.core.create
from pystac import Collection, Item, MediaType
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.raster import RasterExtension
from stactools.core.io import ReadHrefModifier

from .constants import (
    ASSET_CLASSES,
    CLASSIFICATION_SCHEMA,
    COG_RASTER_BAND,
    COLLECTION_DESCRIPTION,
    COLLECTION_ID,
    COLLECTION_TITLE,
    EXTENT,
    KEYWORDS,
    LANDING_PAGE_LINK,
    LICENSE,
    PROVIDERS,
    AssetType,
)
from .metadata import Metadata


def create_item(
    href: str, read_href_modifier: Optional[ReadHrefModifier] = None
) -> Item:
    """Creates a CDL item from one COG href."""
    metadata = Metadata.from_href(href)
    return _create_item_from_metadata(metadata, read_href_modifier)


def create_item_from_hrefs(
    hrefs: List[str], read_href_modifier: Optional[ReadHrefModifier] = None
) -> Item:
    """Creates a CDL item from multiple COG hrefs.

    If the assets at those hrefs don't have the same geometry or time window,
    this will raise a ValueError.
    """

    metadatas = [Metadata.from_href(href) for href in hrefs]
    return _create_item_from_metadatas(metadatas, read_href_modifier)


def create_collection() -> Collection:
    """Creates the USDA-CDL collection."""

    collection = Collection(
        COLLECTION_ID,
        COLLECTION_DESCRIPTION,
        title=COLLECTION_TITLE,
        license=LICENSE,
        keywords=KEYWORDS,
        providers=PROVIDERS,
        extent=EXTENT,
    )
    collection.add_link(LANDING_PAGE_LINK)

    asset_definitions = {}
    for asset_type in AssetType:
        asset_definition = AssetDefinition.create(
            title=None, description=None, media_type=MediaType.COG, roles=["data"]
        )
        asset_definition.properties["raster:bands"] = [
            COG_RASTER_BAND[asset_type].to_dict()
        ]
        classes = ASSET_CLASSES.get(asset_type)
        if classes:
            asset_definition.properties["classification:classes"] = classes
        asset_definitions[asset_type.value] = asset_definition
    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = asset_definitions

    RasterExtension.add_to(collection)
    collection.stac_extensions.append(CLASSIFICATION_SCHEMA)

    return collection


def create_items_from_tiles(
    tiles: List[str], read_href_modifier: Optional[ReadHrefModifier] = None
) -> List[Item]:
    """Creates multiple items from tiles.

    Tiles are grouped by item id, then merged into a single item.
    """
    metadatas: DefaultDict[str, List[Metadata]] = defaultdict(list)
    for tile in tiles:
        metadata = Metadata.from_href(tile)
        if not metadata.tile:
            raise ValueError(f"Not a tile: {metadata.href}")
        metadatas[metadata.item_id].append(metadata)
    items = list()
    for m in metadatas.values():
        item = _create_item_from_metadatas(m, read_href_modifier)
        items.append(item)
    return items


def _create_item_from_metadatas(
    metadatas: List[Metadata], read_href_modifier: Optional[ReadHrefModifier]
) -> Item:
    items = [
        _create_item_from_metadata(metadata, read_href_modifier)
        for metadata in metadatas
    ]
    if not items:
        raise ValueError("No items created")
    base_item = items.pop(0)
    for item in items:
        if item.geometry != base_item.geometry:
            raise ValueError(f"geometry mismatch between items: {base_item}, {item}")
        elif (
            item.common_metadata.start_datetime
            != base_item.common_metadata.start_datetime
        ):
            raise ValueError(
                f"start_datetime mismatch: {item.common_metadata.start_datetime}, "
                f"{base_item.common_metadata.start_datetime}"
            )
        elif (
            item.common_metadata.end_datetime != base_item.common_metadata.end_datetime
        ):
            raise ValueError(
                f"end_datetime mismatch: {item.common_metadata.end_datetime}, "
                f"{base_item.common_metadata.end_datetime}"
            )
        elif item.id != base_item.id:
            raise ValueError(
                f"Component items don't have the same id: {base_item.id}, {item.id}"
            )
        else:
            for key, asset in item.assets.items():
                if key in base_item.assets:
                    raise ValueError(f"asset key {key} already exists in item: {item}")
                base_item.assets[key] = asset
    return base_item


def _create_item_from_metadata(
    metadata: Metadata, read_href_modifier: Optional[ReadHrefModifier]
) -> Item:
    item = stactools.core.create.item(
        metadata.href, read_href_modifier=read_href_modifier
    )
    item.id = metadata.item_id

    item.common_metadata.start_datetime = metadata.start_datetime
    item.common_metadata.end_datetime = metadata.end_datetime
    item.datetime = None
    item.extra_fields["usda_cdl:type"] = metadata.item_type

    asset = item.assets.pop("data")
    asset.title = metadata.cog_title
    asset.media_type = MediaType.COG
    classes = metadata.classes
    if classes:
        asset.extra_fields["classification:classes"] = classes
        item.stac_extensions.append(CLASSIFICATION_SCHEMA)
    item.assets[metadata.asset_type.value] = asset

    asset = item.assets[metadata.asset_type.value]
    raster = RasterExtension.ext(asset, add_if_missing=True)
    raster.bands = metadata.raster_bands

    return item
