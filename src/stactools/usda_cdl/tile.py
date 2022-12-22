import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import rasterio
import rasterio.shutil
import rasterio.windows
from rasterio import DatasetReader, MemoryFile

from .metadata import Metadata

RESOLUTION = 30
DEFAULT_WINDOW_SIZE = 3000  # pixels
DEFAULT_MAX_WORKERS = 8
logger = logging.getLogger(__name__)


@dataclass
class Window:
    """A tile window.

    Contains information about the pixel bounds and the coordinate bounds.
    """

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
        """Returns this tile's name.

        This is used to group tiles by filename when creating items.
        """
        return f"{self.x_min}_{self.y_min}_{self.size}"

    def rasterio_window(self) -> rasterio.windows.Window:
        """Returns the rasterio window, for reading data."""
        return rasterio.windows.Window(
            row_off=self.row_off,
            col_off=self.col_off,
            width=self.width,
            height=self.height,
        )


def tile_zipfile(
    infile: Path,
    directory: Path,
    size: int = DEFAULT_WINDOW_SIZE,
    max_workers: int = DEFAULT_MAX_WORKERS,
    existing_tiles: Optional[List[str]] = None,
) -> List[Path]:
    """Tiles an input GeoTIFF (wrapped in a zipfile)."""
    if infile.suffix != ".zip":
        raise ValueError(f"Infile should end in .zip: {infile}")
    zip_path = f"zip://{infile}!/{infile.stem}.tif"
    with rasterio.open(zip_path) as dataset:
        return _tile_dataset(
            dataset,
            Metadata.from_href(infile.stem),
            directory,
            size,
            max_workers,
            existing_tiles or list(),
        )


def tile_geotiff(
    infile: Path,
    directory: Path,
    size: int = DEFAULT_WINDOW_SIZE,
    max_workers: int = DEFAULT_MAX_WORKERS,
    existing_tiles: Optional[List[str]] = None,
) -> List[Path]:
    """Tiles an input GeoTIFF."""
    with rasterio.open(infile) as dataset:
        return _tile_dataset(
            dataset,
            Metadata.from_href(str(infile)),
            directory,
            size,
            max_workers,
            existing_tiles or list(),
        )


def _tile_dataset(
    dataset: DatasetReader,
    metadata: Metadata,
    directory: Path,
    size: int,
    max_workers: int,
    existing_tiles: List[str],
) -> List[Path]:
    windows = _create_windows(dataset, size)
    read_lock = threading.Lock()

    def tile(window: Window) -> Optional[Path]:
        file_name = f"{metadata.stem}_{window.name()}.tif"
        if file_name in existing_tiles:
            return None
        rasterio_window = window.rasterio_window()
        with read_lock:
            data = dataset.read(1, window=rasterio_window)
        if not data.any():
            return None
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
        path = directory / file_name
        with MemoryFile() as memory_file:
            with memory_file.open(**profile) as open_memory_file:
                open_memory_file.write(data, 1)
                colormap = metadata.colormap
                if colormap:
                    open_memory_file.write_colormap(1, colormap)
                rasterio.shutil.copy(open_memory_file, path, **metadata.cog_profile)
        return path

    paths = list()
    skipped = 0
    written = 0
    num_windows = len(windows)
    interval = int(num_windows / 100) or 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, path in enumerate(executor.map(tile, windows)):
            if path is None:
                skipped += 1
            else:
                written += 1
                paths.append(path)
            if i % interval == 0:
                logger.info(
                    f"[{i + 1}/{num_windows}] written={written}, skipped={skipped}"
                )
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
