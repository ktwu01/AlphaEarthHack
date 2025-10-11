// ============================================
// AlphaEarth Bitcoin Mining Detection Starter
// ============================================

// 1. LOAD ALPHAEARTH EMBEDDINGS
var alphaEarth = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL');

// 2. DEFINE YOUR ANALYSIS PERIOD
var startYear = 2018;  // Match paper's June 2018 start
var endYear = 2024;    // Current available data

// 3. LOAD MINING LOCATIONS FROM CSV
var miningLocations = ee.FeatureCollection('projects/ee-ktwu01/assets/bitcoin-mining')
  .map(function(feature) {
    // Convert CSV data to proper format
    var lat = ee.Number(feature.get('Latitude'));
    var lon = ee.Number(feature.get('Longitude'));
    var country = feature.get('CRCode');
    var countryName = feature.get('CRName');

    return ee.Feature(
      ee.Geometry.Point([lon, lat]),
      {
        label: 1,
        year: 2018,
        location: ee.String(country),
        country_name: countryName
      }
    );
  });

// Visualize all positive mining locations on the map
Map.centerObject(miningLocations, 2);  // Zoom level 2 for global view
Map.addLayer(miningLocations, {color: 'red'}, 'Bitcoin Mining Locations');

// 4. GENERATE NEGATIVE SAMPLES (non-mining locations)
// Best practices for negative sampling:
// 1. Match the geographic distribution of positive samples
// 2. Include diverse land cover types (urban, rural, industrial, natural)
// 3. Use stratified random sampling within same regions
// 4. Aim for balanced dataset (1:1 or up to 1:3 positive:negative ratio)

// Get bounding box of mining locations to constrain negative sampling
var miningBounds = miningLocations.geometry().bounds();

// Get count of positive samples to match
var numPositive = miningLocations.size();
print('Number of mining locations:', numPositive);

// Generate random points within the same geographic regions
// Using stratified sampling to ensure diversity
var negativeLocations = ee.FeatureCollection.randomPoints({
  region: miningBounds,
  points: numPositive,  // Match number of positive samples
  seed: 42,  // For reproducibility
  maxError: 1
}).map(function(feature) {
  return feature.set({
    label: 0,
    year: 2018,
    location: 'negative_sample'
  });
});

// Optional: Filter out negative samples that are too close to mining sites
// This prevents contamination (e.g., excluding points within 1km of mining sites)
var minDistance = 1000;  // meters
negativeLocations = negativeLocations.map(function(negFeature) {
  var distances = miningLocations.map(function(posFeature) {
    return negFeature.geometry().distance(posFeature.geometry());
  });
  var minDist = distances.aggregate_min('distance');
  return negFeature.set('min_distance_to_mining', minDist);
}).filter(ee.Filter.gte('min_distance_to_mining', minDistance));

// 5. COMBINE POSITIVE AND NEGATIVE SAMPLES
var trainingPoints = miningLocations.merge(negativeLocations);

// 6. EXTRACT EMBEDDINGS AT TRAINING POINTS FOR SPECIFIC YEAR
function extractEmbeddings(year) {
  var yearImage = alphaEarth
    .filter(ee.Filter.equals('year', year))
    .first();
  
  // Sample the 64-band embeddings at each point
  var samples = yearImage.sampleRegions({
    collection: trainingPoints,
    scale: 10,  // AlphaEarth is 10m resolution
    geometries: true
  });
  
  return samples;
}

// 7. EXTRACT FOR MULTIPLE YEARS
var embeddings2018 = extractEmbeddings(2018);
var embeddings2021 = extractEmbeddings(2021);  // Pre-China ban
var embeddings2024 = extractEmbeddings(2024);  // Post-ban

// 8. EXPORT FOR CLASSIFIER TRAINING
Export.table.toDrive({
  collection: embeddings2018,
  description: 'AlphaEarth_Mining_Training_2018',
  fileFormat: 'CSV',
  selectors: ['label', 'location', 'year', 'B0', 'B1', 'B2', /* ... B63 */]
});

// 9. VISUALIZE ONE LOCATION
Map.centerObject(miningLocations.first(), 12);
var ae2018 = alphaEarth.filter(ee.Filter.equals('year', 2018)).first();
Map.addLayer(ae2018.select(['B0', 'B1', 'B2']), {min: -1, max: 1}, 'AlphaEarth RGB');
Map.addLayer(miningLocations, {color: 'red'}, 'Mining Locations');

print('Training Points:', trainingPoints.size());
print('AlphaEarth Bands:', ae2018.bandNames());