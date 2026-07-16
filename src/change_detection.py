"""
Core AlphaEarth change detection functions.

All image computation is server-side in Google Earth Engine (lazy evaluation).
Import this module in notebooks instead of redefining these functions locally.

Usage
-----
    from src.change_detection import compute_alpha_layers, smooth_and_mask_alpha

    yod, mag, dur = compute_alpha_layers(geom)
    mag_s, mask, yod_m, mag_m, dur_m = smooth_and_mask_alpha(yod, mag, dur)
"""

import ee

from src.config import (
    ALPHAEARTH_COLLECTION,
    AE_MAG_THRESHOLD,
    AE_SMOOTH_RADIUS,
    AE_SMOOTH_SIGMA,
    AE_YEAR_START,
    AE_YEAR_END,
)


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def normalize_image(img: "ee.Image") -> "ee.Image":
    """L2-normalize all bands of an EE image to the unit hypersphere.

    Parameters
    ----------
    img : ee.Image
        Any multi-band EE image.

    Returns
    -------
    ee.Image
        Same image with all bands divided by their L2 norm (+ 1e-6 epsilon).
    """
    bands = img.bandNames()
    norm = img.select(bands).pow(2).reduce(ee.Reducer.sum()).sqrt().add(1e-6)
    return img.select(bands).divide(norm)


def find_lt_band(img: "ee.Image", key: str) -> "str | None":
    """Return the first band name of *img* whose name contains *key* (case-insensitive).

    Primarily used to locate YOD / MAG / DUR bands in pre-computed LandTrendr assets,
    whose band names vary slightly across assets.

    Parameters
    ----------
    img : ee.Image
        A LandTrendr (or any) EE image.
    key : str
        Substring to search for (e.g. ``'yod'``, ``'mag'``, ``'dur'``).

    Returns
    -------
    str or None
        The matching band name, or ``None`` if no band matches.
    """
    names: list[str] = img.bandNames().getInfo() or []
    return next((b for b in names if key in b.lower()), None)


# ---------------------------------------------------------------------------
# AlphaEarth change pipeline
# ---------------------------------------------------------------------------

def compute_alpha_layers(
    geom: "ee.Geometry",
    change_threshold: float = AE_MAG_THRESHOLD,
    year_start: int = AE_YEAR_START,
    year_end: int = AE_YEAR_END,
) -> "tuple[ee.Image, ee.Image, ee.Image]":
    """Compute AlphaEarth YOD, MAG, and DUR change layers for a geometry.

    Algorithm
    ---------
    1. Load annual AlphaEarth embeddings for each year in [year_start, year_end].
    2. L2-normalize each pixel vector to the unit hypersphere.
    3. Compute cosine similarity for every consecutive year pair.
    4. Select the pair with the *lowest* cosine similarity (highest dissimilarity)
       using a quality mosaic — this defines YOD (year of detection) and MAG.
    5. Count how many pairs exceed *change_threshold* — this defines DUR (duration).

    Parameters
    ----------
    geom : ee.Geometry
        Area of interest.  The collection is filtered and clipped to this geometry.
    change_threshold : float
        Cosine dissimilarity threshold used when counting anomalous years (DUR).
        Default: ``AE_MAG_THRESHOLD`` from ``src.config``.
    year_start : int
        First year of the analysis window (inclusive).  Must be >= 2017.
    year_end : int
        Last year of the analysis window (inclusive).  Must be <= 2024.

    Returns
    -------
    yod : ee.Image
        Single-band image — end-year of the highest-dissimilarity consecutive pair.
        Band name: ``'alpha_yod'``.
    mag : ee.Image
        Single-band image — maximum cosine dissimilarity (0–1).
        Band name: ``'alpha_mag'``.
    dur : ee.Image
        Single-band int16 image — number of consecutive year pairs whose
        dissimilarity exceeded *change_threshold*.
        Band name: ``'alpha_dur'``.
    """
    embeddings = ee.ImageCollection(ALPHAEARTH_COLLECTION)
    years = list(range(year_start, year_end + 1))

    # Load and normalize yearly images clipped to the AOI
    imgs_norm: list["ee.Image"] = []
    for y in years:
        img_y = (
            embeddings
            .filterDate(ee.Date.fromYMD(y, 1, 1), ee.Date.fromYMD(y + 1, 1, 1))
            .filterBounds(geom)
            .mosaic()
            .clip(geom)
        )
        imgs_norm.append(normalize_image(img_y))

    # Cosine similarity images for all consecutive year pairs
    cos_list: list["ee.Image"] = []
    for i in range(len(imgs_norm) - 1):
        imgA = ee.Image(imgs_norm[i])
        imgB = ee.Image(imgs_norm[i + 1])
        cos = imgA.multiply(imgB).reduce(ee.Reducer.sum()).rename("cos")
        pair_year = years[i + 1]
        cos_with_year = cos.addBands(
            ee.Image.constant(pair_year).rename("pair_year").toInt16()
        )
        cos_list.append(cos_with_year)

    cos_ic = ee.ImageCollection.fromImages(cos_list)

    # Quality mosaic: pick the pair with the lowest cosine (= highest dissimilarity)
    scored = cos_ic.map(
        lambda im: ee.Image(im).addBands(
            ee.Image(1).subtract(ee.Image(im).select("cos")).rename("score")
        )
    )
    picked = scored.qualityMosaic("score")

    yod = picked.select("pair_year").rename("alpha_yod")
    mag = ee.Image(1).subtract(picked.select("cos")).rename("alpha_mag")

    # Duration: count pairs whose dissimilarity exceeds the threshold
    inv_ic = cos_ic.sort("pair_year").map(
        lambda im: ee.Image(1).subtract(ee.Image(im).select("cos")).rename("inv")
    )
    dur = (
        inv_ic
        .map(lambda im: ee.Image(im).gt(change_threshold).rename("mask").toInt16())
        .sum()
        .toInt16()
        .rename("alpha_dur")
    )

    return yod, mag, dur


def smooth_and_mask_alpha(
    yod: "ee.Image",
    mag: "ee.Image",
    dur: "ee.Image",
    mag_threshold: float = AE_MAG_THRESHOLD,
    radius: int = AE_SMOOTH_RADIUS,
    sigma: float = AE_SMOOTH_SIGMA,
) -> "tuple[ee.Image, ee.Image, ee.Image, ee.Image, ee.Image]":
    """Apply Gaussian smoothing and a magnitude threshold mask to AlphaEarth layers.

    Parameters
    ----------
    yod, mag, dur : ee.Image
        Raw outputs from :func:`compute_alpha_layers`.
    mag_threshold : float
        Pixels with smoothed MAG > this value are considered changed.
    radius : int
        Gaussian kernel radius in pixels.
    sigma : float
        Gaussian kernel sigma in pixels.

    Returns
    -------
    mag_smoothed : ee.Image
        Smoothed magnitude (unmasked — useful for visualizing the full gradient).
    change_mask : ee.Image
        Binary mask: 1 = changed, 0 = unchanged (based on smoothed MAG).
    yod_masked : ee.Image
        YOD layer masked to change pixels only.
    mag_masked : ee.Image
        Smoothed MAG masked to change pixels only.
    dur_masked : ee.Image
        DUR layer masked to change pixels only.
    """
    kernel = ee.Kernel.gaussian(radius=radius, sigma=sigma, units="pixels")
    mag_smoothed = mag.convolve(kernel)
    change_mask = mag_smoothed.gt(mag_threshold)

    yod_masked = yod.updateMask(change_mask)
    mag_masked = mag_smoothed.updateMask(change_mask)
    dur_masked = dur.updateMask(change_mask)

    return mag_smoothed, change_mask, yod_masked, mag_masked, dur_masked
