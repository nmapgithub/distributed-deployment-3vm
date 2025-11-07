#!/usr/bin/env python3
"""Download OpenStreetMap raster tiles for offline use.

The script fetches XYZ tiles covering a bounding box and saves them under
`core-portal/app/static/tiles/{z}/{x}/{y}.png` so the dashboard can render a
true basemap while offline.

Usage (example):

    python scripts/cache_tiles.py \
        --min-lat 23.5 --min-lon 60.5 \
        --max-lat 37.5 --max-lon 78.0 \
        --zoom 5 6 7 8 9 10 11

Download only what you need and respect the OpenStreetMap tile usage policy:
https://operations.osmfoundation.org/policies/tiles/
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Iterable, Tuple

import requests


ROOT = Path(__file__).resolve().parents[1]
TILE_ROOT = ROOT / "core-portal" / "app" / "static" / "tiles"
MANIFEST_PATH = TILE_ROOT / "manifest.json"
USER_AGENT = "NTRO-Core-TileCacher/1.0 (contact: ops@example.com)"


def deg2num(lat_deg: float, lon_deg: float, zoom: int) -> Tuple[int, int]:
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x_tile = int((lon_deg + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile


def iter_tiles(min_lat: float, min_lon: float, max_lat: float, max_lon: float, zoom_levels: Iterable[int]):
    for zoom in zoom_levels:
        x_min, y_max = deg2num(min_lat, min_lon, zoom)
        x_max, y_min = deg2num(max_lat, max_lon, zoom)

        # ensure ranges are inclusive and correctly ordered
        x_start, x_end = sorted((x_min, x_max))
        y_start, y_end = sorted((y_min, y_max))

        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                yield zoom, x, y


def download_tile(z: int, x: int, y: int, session: requests.Session) -> bytes:
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    response = session.get(url, timeout=15)
    response.raise_for_status()
    return response.content


def ensure_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_manifest(sample_tile: Tuple[int, int, int]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "description": "Auto-generated manifest of cached tiles.",
        "sample_tile": {
            "z": sample_tile[0],
            "x": sample_tile[1],
            "y": sample_tile[2],
        },
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    with MANIFEST_PATH.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cache OpenStreetMap tiles for offline use")
    parser.add_argument("--min-lat", type=float, required=True, help="Southern latitude of bounding box")
    parser.add_argument("--min-lon", type=float, required=True, help="Western longitude of bounding box")
    parser.add_argument("--max-lat", type=float, required=True, help="Northern latitude of bounding box")
    parser.add_argument("--max-lon", type=float, required=True, help="Eastern longitude of bounding box")
    parser.add_argument("--zoom", type=int, nargs="+", required=True, help="One or more zoom levels to cache")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds to sleep between tile downloads")
    parser.add_argument("--overwrite", action="store_true", help="Redownload tiles even if they exist")

    args = parser.parse_args()

    zoom_levels = sorted(set(args.zoom))
    total_tiles = 0

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    sample_tile = None

    print(f"Caching tiles to {TILE_ROOT}")
    for z, x, y in iter_tiles(args.min_lat, args.min_lon, args.max_lat, args.max_lon, zoom_levels):
        target_path = TILE_ROOT / str(z) / str(x) / f"{y}.png"
        if target_path.exists() and not args.overwrite:
            if sample_tile is None:
                sample_tile = (z, x, y)
            continue

        try:
            ensure_directory(target_path)
            image = download_tile(z, x, y, session)
        except requests.HTTPError as http_err:
            print(f"HTTP error for {z}/{x}/{y}: {http_err}", file=sys.stderr)
            continue
        except requests.RequestException as req_err:
            print(f"Request error for {z}/{x}/{y}: {req_err}", file=sys.stderr)
            time.sleep(args.delay * 2)
            continue

        target_path.write_bytes(image)
        total_tiles += 1
        sample_tile = sample_tile or (z, x, y)

        print(f"Saved tile z={z} x={x} y={y}")
        time.sleep(args.delay)

    if sample_tile:
        write_manifest(sample_tile)
        print(f"Manifest updated with sample tile {sample_tile}")
    else:
        print("No new tiles downloaded; manifest left unchanged")

    print(f"Completed. Downloaded {total_tiles} new tiles.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

