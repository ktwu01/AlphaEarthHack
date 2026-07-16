"""
Shared Google Earth Engine visualization parameters for change detection layers.

Import these instead of redefining palettes in each notebook.

Usage
-----
    from src.visualization import VIS_YOD, VIS_MAG_AE, VIS_MAG_LT, VIS_DUR

    Map.addLayer(yod_layer, VIS_YOD, "Year of Detection")
"""

# Year of Detection — cool-to-warm by year (2017 = blue, 2024 = dark red)
VIS_YOD: dict = {
    "min": 2017,
    "max": 2024,
    "palette": [
        "#2166ac",  # 2017 — blue
        "#4393c3",  # 2018
        "#92c5de",  # 2019
        "#fddbc7",  # 2020
        "#d6604d",  # 2021
        "#b2182b",  # 2022
        "#67001f",  # 2023/2024 — dark red
    ],
}

# Magnitude — AlphaEarth cosine dissimilarity (0 – 0.5)
VIS_MAG_AE: dict = {
    "min": 0,
    "max": 0.5,
    "palette": ["white", "#fee08b", "#f46d43", "#a50026"],
}

# Magnitude — LandTrendr NDVI units ×10 000 (0 – 800)
VIS_MAG_LT: dict = {
    "min": 0,
    "max": 800,
    "palette": ["white", "#fee08b", "#f46d43", "#a50026"],
}

# Duration — number of anomalous years (0 – 7)
VIS_DUR: dict = {
    "min": 0,
    "max": 7,
    "palette": [
        "#ffffff",
        "#f3e5f5",
        "#e1bee7",
        "#ce93d8",
        "#ba68c8",
        "#9c27b0",
        "#6a1b9a",
        "#4a148c",
    ],
}
