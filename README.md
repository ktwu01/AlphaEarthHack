# AlphaEarthHack - UT Austin Geoscience Hackathon

Our project seeks to leverage cutting-edge remote sensing analysis to identify and monitor land cover changes, with a focus on visualizing our changing world With effective and efficient data sources. By integrating advanced algorithms and datasets, we provide a comprehensive tool for understanding the dynamics of our changing planet. This tool will support researchers and the professionals in all different disciplines of geography and geology to detect, measure and analyze the changes that interest them.

Click [here](https://ktwu01.github.io/AlphaEarthHack/) for an **interactive dashboard**.

![dashboard](./images/dashboard.png)

## Mentor

**Dr. Brendon Hall**
Sr. Manager in AI for Energy & Utilities, Deloitte. Our Mentor
integrating physics based models, ML and DS to create transformative software tools for the oil and gas industry.

## Team Alpha

![Meet The Team](./images/Team.png)

| Name | Role | Bio |
| :--- | :--- | :--- |
| **Xihan Yao** | Our Developer | 1st year GRG PhD student, Remote Sensing/GIS, Human-Environment Interactions |
| **Koutian Wu** | Our Developer | 2nd year GEO PhD student, Develop the Noah-MP land surface model, Understand the land surface by integrating physics and AI |
| **Rushi Bhatt** | Our Developer | Senior EVS (GRG) Undergraduate, GeoAI, ML, Sediment/Runoff Routing. "Write Code. Test Code. Push Code. … Save The Planet. (some steps may be missing)." |


## Technical Details

*   **Open Source Libraries & Datasets:** 
    *   Google DeepMind
    *   Google AlphaEarth
    *   LandTrendr
    *   GeoAI
    *   NumPy
    *   tqdm
    *   ipyleaflet
    *   Google Earth Engine
    *   Google Earth Engine map
    *   Leaflet.js
    *   Plotly.js

## Reproducibility

Instructions on how to set up and run your project.

```bash
# Example setup commands
pip install -r requirements.txt
python app.py
```

## Interactive Dashboard Details

The interactive dashboard is built with standard web technologies like HTML, CSS, and JavaScript, and leverages the powerful open-source libraries Leaflet.js and Plotly.js to create interactive maps and data visualizations.

## Presentation & Visualizations

In addition to our [PDF presentation](./presentation.pdf), a key feature of our project is the interactive dashboard that allows for dynamic exploration of the data and results.

Here are some other visualizations from our project:

| Global View | Years Side-By-Side |
| :---: | :---: |
| ![Global View](./images/Global_View.png) | ![Years Side by Side](./images/Years_Side_by_Side.png) |

| Cosine Similarity | Feature Search |
| :---: | :---: |
| ![Cosine Similarity](./images/Cosine_Similarity.png) | ![Search](./images/Search.png) |

| AlphaEarth Magnitude | AlphaEarth Duration |
| :---: | :---: |
| ![AE_Mag_masked_Austin](./images/AE_Mag_masked_Austin.png) | ![AE_Dur_masked_Austin](./images/AE_Dur_masked_Austin.png) |

| LandTrendr Magnitude | LandTrendr Duration |
| :---: | :---: |
| ![LandTrendr_Mag_masked_Austin](./images/LandTrendr_Mag_masked_Austin.png) | ![LandTrendr_Dur_masked_Austin](./images/LandTrendr_Dur_masked_Austin.png) |

| AlphaEarth Sample | Cosine Similarity |
| :---: | :---: |
| ![AE_sample_A01_A16_A09_Austin](./images/AE_sample_A01_A16_A09_Austin.png) | ![AE_sample_cosine_similarity_2023_24_Austin](./images/AE_sample_cosine_similarity_2023_24_Austin.png) |

| AE Mag Austin | AE Yoc masked Austin |
| :---: | :---: |
| ![AE_Mag_Austin](./images/AE_Mag_Austin.png) | ![AE_Yoc_masked_Austin](./images/AE_Yoc_masked_Austin.png) |

| Interactive AE dissimilarity plot TESLA Austin | Interactive AE exporting options TESLA Austin |
| :---: | :---: |
| ![Interactive_AE_dissimilarity_plot_TESLA_Austin](./images/Interactive_AE_dissimilarity_plot_TESLA_Austin.png) | ![Interactive_AE_exporting_options_TESLA_Austin](./images/Interactive_AE_exporting_options_TESLA_Austin.png) |

| Interactive AE layers TESLA Austin | Interactive AE mask Berkeley CA |
| :---: | :---: |
| ![Interactive_AE_layers_TESLA_Austin](./images/Interactive_AE_layers_TESLA_Austin.png) | ![Interactive_AE_mask_Berkeley_CA](./images/Interactive_AE_mask_Berkeley_CA.png) |

| LandTrendr Mag Austin | LandTrendr Yoc masked Austin |
| :---: | :---: |
| ![LandTrendr_Mag_Austin](./images/LandTrendr_Mag_Austin.png) | ![LandTrendr_Yoc_masked_Austin](./images/LandTrendr_Yoc_masked_Austin.png) |


## References and Citations


Brown, C. F., Kazmierski, M. R., Pasquarella, V. J., et al. (2025). *AlphaEarth Foundations: An embedding field model for accurate and in-depth global mapping from sparse label data*. arXiv preprint arXiv:2507.22291. [https://arxiv.org/abs/2507.22291](https://arxiv.org/abs/2507.22291)

da Costa-Luis, C. O. (2019). tqdm: A Fast, Extensible Progress Meter for Python and CLI. *Journal of Open Source Software*, *4*(37), 1277. [https://doi.org/10.21105/joss.01277](https://doi.org/10.21105/joss.01277)

Google DeepMind. (2023). [https://deepmind.google/](https://deepmind.google/)

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, *202*, 18–27. [https://doi.org/10.1016/j.rse.2017.06.031](https://doi.org/10.1016/j.rse.2017.06.031)

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., … Oliphant, T. E. (2020). Array programming with NumPy. *Nature*, *585*, 357–362. [https://doi.org/10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

ipyleaflet developers. (2023). *ipyleaflet* (Version 0.17.2) [Computer software]. [https://github.com/jupyter-widgets/ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet)

Janowicz, K., Gao, S., McKenzie, G., Hu, Y., & Bhaduri, B. (2020). GeoAI: spatially explicit artificial intelligence techniques for geographic knowledge discovery and beyond. *International Journal of Geographical Information Science*, *34*(4), 625–636. [https://doi.org/10.1080/13658816.2019.1684500](https://doi.org/10.1080/13658816.2019.1684500)

Kennedy, R. E., Yang, Z., Gorelick, N., Braaten, J., Cavalcante, L., Cohen, W. B., & Healey, S. (2018). Implementation of the LandTrendr Algorithm on Google Earth Engine. *Remote Sensing*, *10*(5), 691. [https://doi.org/10.3390/rs10050691](https://doi.org/10.3390/rs10050691)

Agafonkin, V., & Leaflet Contributors. (n.d.). *Leaflet: An open-source JavaScript library for interactive maps*. Retrieved October 12, 2025, from https://leafletjs.com

Plotly Technologies Inc. (2015). *Collaborative data science*. Plotly Technologies Inc. https://plot.ly
