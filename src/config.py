"""
Centralized constants for AlphaEarth Change Detection.
Import this module in notebooks to avoid hard-coding asset paths.
"""

# ── Google Earth Engine image collections ─────────────────────────────────────
ALPHAEARTH_COLLECTION = "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL"
"""AlphaEarth 64-band annual satellite embedding composite (2017–2024)."""

# ── Pre-computed LandTrendr GEE assets (one per study site) ───────────────────
# Naming convention: LT_<Site>_<lat>_<lon>_NDVI_2016_2024
LANDTRENDR_ASSETS: dict[str, str] = {
    # Urbanization
    "Austin_TX":      "users/xihanyao/LT_Austin_UrbanGrowth_30_98_NDVI_2016_2024",
    "Dallas_TX":      "users/xihanyao/LT_Dallas_TX_33_97_NDVI_2016_2024",
    "Houston_TX":     "users/xihanyao/LT_Houston_TX_30_95_NDVI_2016_2024",
    "Bend_OR":        "users/xihanyao/LT_Bend_UrbanExpansion_44_121_NDVI_2016_2024",
    "Portland_OR":    "users/xihanyao/LT_Portland_Metro_UrbanGrowth_45_123_NDVI_2016_2024",
    "Sacramento_CA":  "users/xihanyao/LT_Sacramento_UrbanEdge_39_121_NDVI_2016_2024",
    # Wildfires
    "Bootleg_OR":     "users/xihanyao/LT_Bootleg_Fire_2021_43_121_NDVI_2016_2024",
    "CampFire_CA":    "users/xihanyao/LT_CampFire_CA_2018_40_122_NDVI_2016_2024",
    "DixieFire_CA":   "users/xihanyao/LT_DixieFire_CA_2021_40_121_NDVI_2016_2024",
    "MosquitoFire_CA":"users/xihanyao/LT_MosquitoFire_CA_2022_39_121_NDVI_2016_2024",
    "Santiam_OR":     "users/xihanyao/LT_Santiam_Fire_2020_45_122_NDVI_2016_2024",
    # Forest / Logging
    "Angelina_TX":    "users/xihanyao/LT_Angelina_Forest_TX_31_95_NDVI_2016_2024",
    "CoosBay_OR":     "users/xihanyao/LT_CoosBay_IndustrialForestry_43_124_NDVI_2016_2024",
    "MtHood_OR":      "users/xihanyao/LT_MtHood_WUI_Forestry_45_122_NDVI_2016_2024",
    "ShastaTrinity_CA":"users/xihanyao/LT_ShastaTrinity_Timberlands_41_122_NDVI_2016_2024",
}

# ── Change detection thresholds ───────────────────────────────────────────────
AE_MAG_THRESHOLD = 0.15        # cosine dissimilarity
LT_MAG_THRESHOLD = 170         # NDVI units (×10 000 scale)

AE_SMOOTH_RADIUS = 2           # Gaussian kernel radius (pixels)
AE_SMOOTH_SIGMA  = 1           # Gaussian sigma

# ── Temporal range ────────────────────────────────────────────────────────────
AE_YEAR_START = 2017
AE_YEAR_END   = 2024
LT_YEAR_START = 2016
LT_YEAR_END   = 2024
