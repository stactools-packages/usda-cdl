from pathlib import Path

from stactools.usda_cdl import tile


def test_tile_cdl(cdl: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(cdl, tmp_path, 500)
    assert len(paths) == 4


def test_tile_cdl_existing_tiles(cdl: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(
        cdl, tmp_path, 500, existing_tiles=["2021_30m_cdls_-91095_1807575_15000.tif"]
    )
    assert len(paths) == 3


def test_tile_confidence(confidence: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(confidence, tmp_path, 500)
    assert len(paths) == 4


def test_tile_cultivated(cultivated: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(cultivated, tmp_path, 500)
    assert len(paths) == 4


def test_tile_corn(corn: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(corn, tmp_path, 500)
    assert len(paths) == 4


def test_tile_cotton(cotton: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(cotton, tmp_path, 500)
    assert len(paths) == 4


def test_tile_soybeans(soybeans: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(soybeans, tmp_path, 500)
    assert len(paths) == 4


def test_tile_wheat(wheat: Path, tmp_path: Path) -> None:
    paths = tile.tile_geotiff(wheat, tmp_path, 500)
    assert len(paths) == 4
