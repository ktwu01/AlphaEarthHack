document.addEventListener('DOMContentLoaded', function () {
    // ========== MAP INITIALIZATION ==========
    var mymap = L.map('mapid').setView([30.209732, -97.6589635], 12); // Austin centered
    
    // Satellite base layer
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 14,
        attribution: 'Esri'
    }).addTo(mymap);

    // Define Austin polygon coordinates
    var austinPolygon = [
        [30.150367, -97.583924],
        [30.150367, -97.734003],
        [30.269097, -97.734003],
        [30.269097, -97.583924]
    ];

    // Create the polygon and add it to the map
    L.polygon(austinPolygon, {
        color: 'yellow',
        fillColor: '#f03',
        fillOpacity: 0.2
    }).addTo(mymap).bindPopup("Austin, TX Analysis Region");
    
    
    // ========== PLOTLY CHART DATA ==========
    const plotData = {
        "labels": [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "datasets": [
            { "label": "Median (p50)", "data": [0.9512, 0.9395, 0.9629, 0.9629, 0.959, 0.9708, 0.9551] },
            { "label": "Trimmed mean (10 to 90%)", "data": [0.9463, 0.9376, 0.9604, 0.9606, 0.958, 0.9673, 0.9535] },
            { "label": "IQR (p75 to p25)", "data": [0.039, 0.0429, 0.0273, 0.0272, 0.0233, 0.0234, 0.0273] },
            { "label": "StdDev", "data": [0.0395, 0.0458, 0.0463, 0.0492, 0.046, 0.0552, 0.047] },
            { "label": "Frac < 0.95", "data": [0.5092, 0.6367, 0.2897, 0.284, 0.3083, 0.2053, 0.4024] }
        ]
    };

    // Helper to get dataset by label
    function getDataset(label) {
        return plotData.datasets.find(d => d.label === label).data;
    }

    // ========== CREATE PLOTS ==========
    const plotlyConfig = { responsive: true };

    // 1) Central tendency
    const trace1 = {
        x: plotData.labels,
        y: getDataset('Median (p50)'),
        mode: 'lines+markers',
        name: 'Median (p50)'
    };
    const trace2 = {
        x: plotData.labels,
        y: getDataset('Trimmed mean (10 to 90%)'),
        mode: 'lines+markers',
        name: 'Trimmed mean (10–90%)'
    };
    const layout1 = {
        title: 'Central Tendency',
        yaxis: { title: 'Cosine similarity', range: [0.9, 1.0], domain: [0, 1] },
        xaxis: { title: 'Year', domain: [0.01, 0.99] },
        margin: { l: 80, r: 50, t: 50, b: 50 }
    };
    Plotly.newPlot('plot1', [trace1, trace2], layout1, plotlyConfig);

    // 2) Spread
    const trace3 = {
        x: plotData.labels,
        y: getDataset('IQR (p75 to p25)'),
        mode: 'lines+markers',
        name: 'IQR (p75–p25)'
    };
    const trace4 = {
        x: plotData.labels,
        y: getDataset('StdDev'),
        mode: 'lines+markers',
        name: 'StdDev'
    };
    const layout2 = {
        title: 'Spread',
        yaxis: { title: 'Spread', domain: [0, 1] },
        xaxis: { title: 'Year', domain: [0.01, 0.99] },
        margin: { l: 80, r: 50, t: 50, b: 50 }
    };
    Plotly.newPlot('plot2', [trace3, trace4], layout2, plotlyConfig);

    // 3) Area fraction below threshold
    const trace5 = {
        x: plotData.labels,
        y: getDataset('Frac < 0.95'),
        type: 'bar',
        name: 'Frac < 0.95'
    };
    const layout3 = {
        title: 'Area Fraction Below Threshold',
        yaxis: { title: 'Frac < 0.95' },
        xaxis: { title: 'Year' }
    };
    Plotly.newPlot('plot3', [trace5], layout3, plotlyConfig);
});