# AlphaEarth Bitcoin Mining Analysis Plan

## Background and Motivation

The goal of this project is to analyze land use changes at known bitcoin mining locations using Google Earth Engine (GEE). We will leverage the `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` (referred to as AlphaEarth) dataset, which provides annual semantic embeddings of satellite imagery.

The primary analysis method will be to calculate the cosine similarity of these embeddings over time for each location. A lower cosine similarity between two years indicates a more significant change in the land's characteristics as captured by the satellite.

The final deliverable will be a dataset, likely in GeoJSON format, that can be used to power an interactive web map. This map will display the mining locations, and clicking on a location will reveal a chart showing the changes in cosine similarity over the years. This will allow for the visual exploration of how these sites have evolved, potentially correlating changes with real-world events like policy shifts.

The existing notebook (`GEE-test.ipynb`) has successfully demonstrated the feasibility of extracting embeddings and performing a basic analysis but requires significant refactoring and enhancement to achieve the final vision.

## Key Challenges and Analysis

Based on the successful `austin_change.ipynb` tutorial, we can refine our understanding of the challenges and the best path forward.

1.  **Server-Side Computation is Key**: The Austin notebook demonstrates that the entire time-series analysis, including calculating cosine similarity for a region, can be done efficiently on G-E-E's servers. The previous approach of exporting raw embeddings to CSVs was inefficient and unnecessary. Our primary challenge is to adapt this server-side pattern to work for thousands of individual mining locations instead of just one large area.
2.  **Point vs. Area-Based Analysis**: The need for area-based analysis is confirmed. The Austin notebook uses a single polygon. We will adapt this by creating a buffer (a circular polygon) around each mining location point. The core task is to map the analysis function over our entire collection of buffered points.
3.  **Efficient Data Extraction**: The Austin notebook extracts only the final, aggregated metrics (`.aggregate_array()`). This is far more efficient than exporting large tables. We will adopt this, exporting only the calculated time-series data for each location.
4.  **Time-Series Data Generation**: The Austin notebook calculates year-over-year similarity (`2017-2018`, `2018-2019`, etc.). For our goal, it's more useful to compare each year against a fixed baseline (e.g., 2018). This shows the cumulative change from the start. We will adapt the logic to calculate the similarity of 2019, 2020, 2021, etc., all relative to 2018.
5.  **Data Export for Visualization**: GeoJSON remains the correct target format. The challenge is to structure our server-side GEE workflow to build a `FeatureCollection` where each feature has the necessary properties (location name, country, and the time-series data) before the final export.

## High-level Task Breakdown

The project will be broken down into the following distinct tasks. This revised plan emphasizes server-side processing based on the Austin notebook's methodology. The Executor should address these one by one.

1.  **Consolidate Successful Code**: Copy the successful, essential setup cells from `GEE-test.ipynb` into the new `GEE_Time_Series_Analysis.ipynb` notebook. This includes GEE initialization, loading the Bitcoin mining locations `FeatureCollection`, and generating the negative sample points. This will create a solid, runnable foundation based on previously validated work.
2.  **Develop Server-Side Analysis Functions**: Port and adapt the logic from the Austin notebook to work with our specific data.
    -   Create a function `get_mean_embedding(year, geometry)` that takes a year and a geometry (our buffer), mosaics the annual AlphaEarth image for that year, and returns a single `ee.Dictionary` containing the mean embedding vector for that area using `image.reduceRegion()`.
    -   Create a function `get_cosine_similarity(embedding1, embedding2)` that takes two embedding dictionaries (from the previous function) and calculates the cosine similarity, returning a single `ee.Number`. This will be a pure server-side calculation.
3.  **Map Analysis Over All Locations and Years**: This is the core computational step.
    -   Define a baseline year (e.g., 2018) and a range of years to analyze (e.g., 2017-2024).
    -   Create a function that can be mapped over the `ee.FeatureCollection` of mining locations. For each location (feature), this function will:
        -   Create a buffer geometry around the point.
        -   Calculate the mean embedding for the baseline year.
        -   Iterate through the analysis years, calculating the mean embedding for each year and its cosine similarity relative to the baseline embedding.
        -   Store the results as a dictionary or list in a new property on the feature (e.g., `{'2019': 0.98, '2020': 0.95, ...}`).
        -   Return the feature with the new time-series property.
4.  **Export Time-Series Data to GeoJSON**:
    -   Execute the mapping operation from the previous step on the full collection of mining sites. This produces a new `FeatureCollection` where each feature is enriched with its similarity time-series data.
    -   Use `ee.batch.Export.table.toGeoJSON()` to export this final `FeatureCollection` directly to a GeoJSON file in Google Drive. This avoids intermediate CSV files entirely.
5.  **Visualize Results from GeoJSON**:
    -   Load the exported GeoJSON file into the notebook using `geemap`.
    -   Create an interactive map displaying the mining locations. Configure the map so that clicking on a point displays its time-series data (this can be a simple printout of the properties for validation).

## Project Status Board

-   [x] **Task 1: Consolidate Successful Code**
    -   **Success Criteria**: The `GEE_Time_Series_Analysis.ipynb` notebook contains and can successfully execute the code for: 1. Authenticating and initializing Earth Engine. 2. Loading the `miningLocations` `FeatureCollection`. 3. Merging it with `negativeLocations` to create the `trainingPoints` `FeatureCollection`.
-   [ ] **Task 2: Develop Server-Side Analysis Functions**
    -   **Success Criteria**: The notebook contains two well-defined Python functions, `get_mean_embedding` and `get_cosine_similarity`, that perform their calculations entirely with Earth Engine objects (`ee.Image`, `ee.Reducer`, `ee.Dictionary`, `ee.Number`) and do not call `.getInfo()`.
-   [ ] **Task 3: Map Analysis Over All Locations and Years**
    -   **Success Criteria**: A Python function is created that takes a single `ee.Feature` (a mining site), applies the buffering and time-series analysis, and returns the feature with a new property (e.g., `similarity_ts`) containing the similarity scores for each year. This function can be successfully mapped over a small test set of the mining locations (e.g., `.limit(5)`).
-   [ ] **Task 4: Export Time-Series Data to GeoJSON**
    -   **Success Criteria**: An export task is successfully started using `ee.batch.Export.table.toGeoJSON()`. The task runs and completes, producing a `mining_similarity.geojson` file in Google Drive. The file is valid GeoJSON.
-   [ ] **Task 5: Visualize Results from GeoJSON**
    -   **Success Criteria**: The `mining_similarity.geojson` file is loaded into the notebook using `geemap`. A map is rendered, and clicking on a location correctly displays the properties, including the `similarity_ts` data.

## Executor's Feedback or Assistance Requests

*This section is for the Executor to fill out as tasks are completed or if issues arise.*
- **Task 1 Complete**: I have consolidated the successful code from `GEE-test.ipynb` into the new `GEE_Time_Series_Analysis.ipynb` notebook. The notebook now has a solid foundation for GEE initialization, loading the mining locations, and generating negative samples. Ready to proceed to Task 2.

## Lessons

*This section is for documenting key learnings during the process.*
- **Lesson 1**: Avoid using `.getInfo()` on large GEE FeatureCollections to prevent server timeouts. Use `ee.batch.Export` for any heavy computation or data extraction.
- **Lesson 2**: When combining pandas DataFrames from different sources that represent the same entities, `pd.merge` on a common key (`point_id`) is more reliable than `pd.concat`. Ensure data is filtered for completeness (`dropna`) before processing to avoid errors with `NaN` values.
