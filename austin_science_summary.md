# Austin Cosine Similarity (2017–2024) — Scientific Summary

## Context
- Region: Austin AOI polygon `[[-97.583924, 30.150367], [-97.734003, 30.150367], [-97.734003, 30.269097], [-97.583924, 30.269097]]`
- Years: 2017–2024 (visualized 2018–2024)
- Metric: Annual per-pixel embedding cosine similarity relative to baseline; aggregated region-wide
- Summary statistics: Median (p50), trimmed mean (10–90%), IQR (p75–p25), StdDev, and fraction of pixels with similarity < 0.95

## Key observations
- Central tendency rises notably from 2019 → 2020 (Median 0.9395 → 0.9629; Trimmed mean 0.9376 → 0.9604).
- Spread tightens in 2020: IQR drops 0.0429 → 0.0273; StdDev remains comparable (0.0458 → 0.0463).
- Fraction below 0.95 declines sharply: 0.6367 → 0.2897.

Together, these indicate the distribution shifted upward and became more concentrated around higher similarity values in 2020.

## Why might IQR drop in 2020?
Hypotheses (not mutually exclusive):
1. Regional homogenization of surface signals
   - Broad-scale vegetation/water/soil conditions became more uniform across the AOI (e.g., synchronized phenology or moisture), compressing the distribution.
2. Acquisition/processing effects
   - Improved cloud/shadow masking, different seasonal alignment, or data density changes reduce noisy tails and narrow spread.
3. Sensor/stack composition
   - Mix of sensors, revisit cadence, or quality filters changed between years, altering variance.
4. Socio-environmental changes (COVID period)
   - Reduced human activity can modulate urban/rural spectral patterns (traffic, industrial activity), potentially making embeddings more uniform; needs careful attribution.
5. Hydroclimate anomaly
   - Precipitation/temperature anomalies could drive consistent vegetation responses across the AOI, reducing dispersion.

## Quick checks to discriminate causes
- Hold-out QC:
  - Match acquisition windows (month/day) across years to control seasonality.
  - Enforce consistent cloud/shadow masks and minimum observation counts per pixel per year.
- Stratified analysis:
  - Compute stats by land-cover class (urban, vegetation, water) to see where IQR compression occurs.
  - Map per-pixel deltas and IQR contributions; check if edges or specific subregions dominate.
- Sampling/statistical rigor:
  - Report sample sizes per year; bootstrap CIs for p50/IQR/mean.
  - Use robust spread metrics beyond IQR (e.g., MAD) as sensitivity check.
- Cross-region controls:
  - Compare with a nearby region with similar climate/land cover to test regional vs. local drivers.

## Interpretation notes
- The simultaneous increase in median and drop in IQR suggests a systematic shift rather than random noise reduction alone.
- Attribution to COVID-related changes is plausible but not conclusive without controlling for seasonality, QC, and hydroclimate.

## Next steps
- Recompute annual stats with:
  - Fixed seasonal windows and identical masks.
  - Per-class stratification and per-pixel observation counts.
  - Bootstrap uncertainty bands for p50 and IQR.
- Add a small multiples view: per-class central tendency and spread over time.
- Document data lineage (sensors, masks, thresholds) for reproducibility.
