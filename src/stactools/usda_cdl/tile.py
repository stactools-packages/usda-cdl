from dataclasses import dataclass
from pathlib import Path
from typing import List

import rasterio
import rasterio.shutil
import rasterio.windows
from rasterio import DatasetReader, MemoryFile

from .metadata import Metadata

RESOLUTION = 30
DEFAULT_WINDOW_SIZE = 3000  # pixels


@dataclass
class Window:
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    row_off: int
    col_off: int
    width: int
    height: int
    size: int

    def name(self) -> str:
        return f"{self.x_min}_{self.y_min}_{self.size}"

    def rasterio_window(self) -> rasterio.windows.Window:
        return rasterio.windows.Window(
            row_off=self.row_off,
            col_off=self.col_off,
            width=self.width,
            height=self.height,
        )


def tile_zipfile(
    infile: Path, directory: Path, size: int = DEFAULT_WINDOW_SIZE
) -> List[Path]:
    """Tiles an input GeoTIFF (wrapped in a zipfile)."""
    if infile.suffix != ".zip":
        raise ValueError(f"Infile should end in .zip: {infile}")
    zip_path = f"zip://{infile}!/{infile.stem}.tif"
    with rasterio.open(zip_path) as dataset:
        return _tile_dataset(dataset, Metadata.from_href(infile.stem), directory, size)


def tile_geotiff(
    infile: Path, directory: Path, size: int = DEFAULT_WINDOW_SIZE
) -> List[Path]:
    """Tiles an input GeoTIFF."""
    with rasterio.open(infile) as dataset:
        return _tile_dataset(dataset, Metadata.from_href(str(infile)), directory, size)


def _tile_dataset(
    dataset: DatasetReader, metadata: Metadata, directory: Path, size: int
) -> List[Path]:
    windows = _create_windows(dataset, size)
    paths = list()
    for window in windows:
        rasterio_window = window.rasterio_window()
        data = dataset.read(1, window=rasterio_window)
        if not data.any():
            continue
        transform = dataset.window_transform(rasterio_window)
        profile = {
            "driver": "GTiff",
            "width": window.width,
            "height": window.height,
            "count": 1,
            "dtype": "uint8",
            "transform": transform,
            "crs": dataset.crs,
        }
        path = directory / f"{metadata.stem}_{window.name()}.tif"
        with MemoryFile() as memory_file:
            with memory_file.open(**profile) as open_memory_file:
                open_memory_file.write(data, 1)
                colormap = metadata.colormap
                if colormap:
                    open_memory_file.write_colormap(1, colormap)
                rasterio.shutil.copy(open_memory_file, path, **metadata.cog_profile)
        paths.append(path)
    return paths


def _create_windows(dataset: DatasetReader, size: int) -> List[Window]:
    if dataset.res != (RESOLUTION, RESOLUTION):
        raise ValueError(f"Dataset has unexpected resolution: {dataset.res}")
    height, width = dataset.shape
    row = 0
    col = 0
    windows = list()
    while row < height:
        windows.append(
            Window(
                x_min=int(dataset.bounds.left + col * RESOLUTION),
                y_min=int(dataset.bounds.top - (row + 1) * RESOLUTION),
                x_max=int(dataset.bounds.left + (col + 1) * RESOLUTION),
                y_max=int(dataset.bounds.top - row * RESOLUTION),
                col_off=col,
                row_off=row,
                width=size,
                height=size,
                size=size * RESOLUTION,
            )
        )
        col += size
        if col > width:
            col = 0
            row += size
    return windows
