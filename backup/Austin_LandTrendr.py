import os
import ee
import geemap

# -----------------------------
# 0) Initialize Earth Engine
# -----------------------------
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()

# -----------------------------
# 1) AOI & time window
# -----------------------------
austin = ee.Geometry.Rectangle([-98.0, 30.1, -97.6, 30.5], geodesic=False)
startYear, endYear = 2016, 2024
startDay, endDay = '01-01', '12-31'   # try ('06-01','09-30') to reduce seasonality

# -----------------------------
# 2) Landsat SR → NDVI helpers
# -----------------------------
QA_BITS = dict(cirrus=2, cloud=3, shadow=4, snow=5)

def mask_landsat_sr(img: ee.Image) -> ee.Image:
    qa = img.select('QA_PIXEL')
    def ok(bit): return qa.bitwiseAnd(1 << QA_BITS[bit]).eq(0)
    clear = ok('cirrus').And(ok('cloud')).And(ok('shadow')).And(ok('snow'))
    return img.updateMask(clear)

def add_ndvi_l57(img: ee.Image) -> ee.Image:
    return img.addBands(img.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI'))

def add_ndvi_l89(img: ee.Image) -> ee.Image:
    return img.addBands(img.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI'))

def annual_ndvi_image(year: int) -> ee.Image:
    start = ee.Date.fromYMD(year, int(startDay[:2]), int(startDay[3:]))
    end   = ee.Date.fromYMD(year, int(endDay[:2]),   int(endDay[3:]))
    l5 = (ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
          .filterBounds(austin).filterDate(start, end).map(mask_landsat_sr).map(add_ndvi_l57))
    l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
          .filterBounds(austin).filterDate(start, end).map(mask_landsat_sr).map(add_ndvi_l57))
    l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
          .filterBounds(austin).filterDate(start, end).map(mask_landsat_sr).map(add_ndvi_l89))
    l9 = (ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')
          .filterBounds(austin).filterDate(start, end).map(mask_landsat_sr).map(add_ndvi_l89))
    return (l5.merge(l7).merge(l8).merge(l9)).select('NDVI').median().rename(str(year))

years = list(range(startYear, endYear + 1))
ndvi_stack = ee.Image.cat([annual_ndvi_image(y) for y in years]).clip(austin)
ndvi_stack_i16 = ndvi_stack.multiply(1000).toInt16()

# -----------------------------
# 3) LandTrendr
# -----------------------------
lt = ee.Algorithms.TemporalSegmentation.LandTrendr(
    timeSeries=ndvi_stack_i16,
    maxSegments=6,
    spikeThreshold=0.9,
    vertexCountOvershoot=3,
    preventOneYearRecovery=True,
    recoveryThreshold=0.25,
    pvalThreshold=0.05,
    bestModelProportion=0.75,
    minObservationsNeeded=6
)

# -----------------------------
# 4) Greatest NDVI LOSS segment
#    (drop singleton row axis!)
# -----------------------------
V = lt.select('LandTrendr')               # [2 x nVerts]
years_arr = V.arraySlice(0, 0, 1)         # [1 x nVerts]
fit_arr   = V.arraySlice(0, 1, 2)         # [1 x nVerts]

# Make arrays rank-1 [nVerts] by dropping axis 0:
years_arr = years_arr.arrayProject([1])   # [nVerts]
fit_arr   = fit_arr.arrayProject([1])     # [nVerts]

# Build segments [nSeg]
y_start = years_arr.arraySlice(0, 0, -1)  # [nSeg]
y_end   = years_arr.arraySlice(0, 1, None)
v_start = fit_arr.arraySlice(0, 0, -1)
v_end   = fit_arr.arraySlice(0, 1, None)

dur     = y_end.subtract(y_start)         # [nSeg]
mag     = v_end.subtract(v_start)         # [nSeg] Δ(NDVI×1000)
abs_mag = mag.abs()

in_window = y_end.gte(startYear).And(y_end.lte(endYear))
valid_dur = dur.gt(0)
loss      = mag.lt(0)

valid_i   = loss.And(in_window).And(valid_dur).toInt16()  # 0/1 array [nSeg]
invalid_i = valid_i.Not().toInt16()
NEG_BIG   = ee.Image.constant(-1000000000).toInt16()

# score = |Δ| for valid, NEG_BIG for invalid (pure arithmetic; no where)
scored = abs_mag.multiply(valid_i).add(NEG_BIG.multiply(invalid_i))  # [nSeg]

# Max score per pixel (array length 1), and one-hot selector [nSeg]
max_score = scored.arrayReduce(ee.Reducer.max(), [0])  # [1]
selector  = scored.eq(max_score).toInt16()             # [nSeg] 0/1

# Select attributes via one-hot * then sum over segments
sel_yod = y_end.multiply(selector).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0]).toInt16()
sel_dur = dur  .multiply(selector).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0]).toInt16()
sel_mag = abs_mag.multiply(selector).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0]).toInt16()

# Mask pixels with no valid loss (max_score == NEG_BIG)
has_event = max_score.arrayGet([0]).gt(NEG_BIG.add(1))
change_img = ee.Image.cat([
    sel_yod.rename('yod'),
    sel_mag.rename('mag'),
    sel_dur.rename('dur')
]).updateMask(has_event).clip(austin)

# -----------------------------
# 5) Export multiband GeoTIFF
# -----------------------------
# Use a plain local folder (adjust if needed)
out_dir = os.path.expanduser("~/gee_exports_local")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "Austin_LT_YOD_MAG_DUR_2016_2024.tif")
print("Saving multiband GeoTIFF to:", out_path)

def export_local(img, path):
    geemap.ee_export_image(
        img.select(['yod', 'mag', 'dur']),
        filename=path,
        scale=30,
        region=austin,
        file_per_band=False
    )

try:
    export_local(change_img, out_path)
    print("✅ Local download complete.")
except Exception as e:
    print("⚠️ Local download failed; starting Drive export.\n ", e)
    task = ee.batch.Export.image.toDrive(
        image=change_img.select(['yod','mag','dur']).toInt16(),
        description='Austin_LT_YOD_MAG_DUR_2016_2024',
        folder='ee_exports',
        fileNamePrefix='Austin_LT_YOD_MAG_DUR_2016_2024',
        region=austin,
        scale=30,
        maxPixels=1e13
    )
    task.start()
    print("📦 Drive export started. Check the Tasks tab / Drive when it finishes.")
