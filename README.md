# AlphaEarthHack
UT Austin Geoscience Hackathon: `AlphaEarthHack` team

# All the data are fake now!!!

change the theme. 1. delete emoji, 2. add annotations to each necesary place saying 'these are only mock  data' 3. remove fancy frame with lots of embedding colors. (keep current dot colors for intersting points.)

Can this be deployed on GitHub pages instead? I think if we do not require so many dynamic objects, we can do it static.

- [ ] Idea: e.g. input a city, calculate its nearest point (this point can be updated later).

✅ **Interactive Leaflet map** with fire/drought markers  
✅ **Chart.js time series** showing 2017-2024 trends  
✅ **Mobile responsive** design  
✅ **Easy to update** - just replace placeholder data in the `locations` array and chart data

## To Deploy on GitHub Pages:

1. **Save as `index.html`** in your repo
2. **Add placeholder images** (optional): Create `img/leaflet-images/` folder if you want custom markers
3. **Push to GitHub** and enable Pages in Settings
4. **Generate QR code** to your `username.github.io/repo-name`

## To Add Your Real Data:

Replace the `locations` array and chart `data` arrays with your AlphaEarth analysis results. For example:

```javascript
const locations = [
    {
        name: "Your Location",
        lat: 34.416,
        lng: -119.845,
        fireRisk: 85,  // From your model
        droughtSeverity: "Severe",  // From your analysis
        trend: "Increasing",
        color: "#d32f2f"  // Red for high risk
    }
];
```
