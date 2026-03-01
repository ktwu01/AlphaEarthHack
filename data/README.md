# data/

This directory is for locally downloaded raster files or GeoTIFFs used during development.
It is **git-ignored** — do not commit large binary files here.

All primary data is accessed server-side via Google Earth Engine (no local download needed).

## Pre-computed GEE Assets (read by notebooks)

LandTrendr outputs for all 15 study sites are stored as GEE assets. The asset IDs are
defined in `src/config.py`. No local data download is required to run the main notebooks.
