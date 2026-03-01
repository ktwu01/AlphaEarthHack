# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UT Austin Geoscience Hackathon project by Team Alpha. Analyzes land use and environmental change using **AlphaEarth** satellite embeddings (64-dimensional AI vectors) and **LandTrendr** (traditional NDVI-based spectral-temporal change detection), comparing both methods across 15 study sites in the western United States.

## Environment Setup

No requirements file exists. Key dependencies (install via pip or conda):

```bash
pip install earthengine-api geemap numpy pandas matplotlib seaborn scipy ipyleaflet ipywidgets
```

Authenticate with Google Earth Engine before running notebooks:

```bash
earthengine authenticate
```

All notebooks require an active GEE session (`ee.Initialize()`).

## Notebook Architecture

The project is entirely notebook-based — no standalone scripts are used in the main workflow.

### Main Notebooks (run in this order for full analysis):

| Notebook | Purpose |
|---|---|
| `alpha_tutorial.ipynb` | Introductory tutorial: AlphaEarth K-means clustering |
| `AlphaEarth_Story.ipynb` | Primary narrative: cosine similarity, dam detection, Austin urban growth |
| `AlphaEarth_Interactive_Mapping.ipynb` | Interactive AOI drawing, real-time change detection, export tools |
| `AlphaEarth_LandTrendr_ChangeComparison.ipynb` | Side-by-side comparison of both algorithms across 15 sites + IoU analysis |
| `LandTrendr_AlphaEarth.ipynb` | Deep-dive LandTrendr analysis, statistical summaries, CSV exports |

### Backup notebooks in `/backup/`:
- `AlphaEarth_EDA.ipynb`, `LandTrendr_EDA.ipynb` — exploratory/tuning work
- `Austin_LandTrendr_Changes.ipynb` — Austin-specific analysis
- `Austin_LandTrendr.py` — standalone script version

## Key Data Sources (Google Earth Engine)

- **AlphaEarth embeddings**: `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` — 64-band annual composite, 2017–2024
- **LandTrendr outputs**: 15 pre-computed GEE assets (one per study site), 2016–2024 NDVI-based
- **Landsat**: Used internally by LandTrendr for NDVI computation

## Change Detection Methodology

Both algorithms output three standardized layers:
- **YOD** — Year of first detected change
- **MAG** — Magnitude of change
- **DUR** — Duration (consecutive high-change years)

**AlphaEarth pipeline**: Cosine similarity between embedding years → Gaussian smoothing (kernel radius=2, sigma=1) → threshold >0.15 → morphological operations

**LandTrendr pipeline**: NDVI spectral trajectory fitting → threshold >170 NDVI units → same morphological cleanup

**Validation**: IoU (Intersection over Union) computed between both methods' binary change masks per site.

## Study Sites

**Urbanization**: Austin TX, Dallas TX, Houston TX, Bend OR, Portland OR, Sacramento CA
**Wildfires**: Bootleg OR (2021), Camp Fire CA (2018), Dixie CA (2021), Mosquito CA (2022), Santiam OR (2020)
**Forest/Logging**: Angelina TX, Coos Bay OR, Mt Hood OR, Shasta-Trinity CA

## Interactive Features

`AlphaEarth_Interactive_Mapping.ipynb` provides:
- Draw AOI on map → auto-computes change layers server-side in GEE
- Inspector tool: click any point to see year-by-year similarity chart
- Sliders: magnitude threshold, smoothing radius/sigma, layer opacity
- Export to GEE Asset or Google Drive

## Output Files

- `lt_training_stats_all_assets.csv` — per-band stats for all 15 LandTrendr assets
- `lt_training_corr_all_assets.csv` — inter-band correlations
- `lt_training_asset_summary.csv` — training pixel counts and areas
- `images/IoU_LandTrendr_AlphaEarth_15sites.png` — comparison result figure
- `UT_GIS_map/` — exported map PNGs for Austin/UT campus change layers
