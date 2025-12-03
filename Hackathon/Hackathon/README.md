# 🛰️ CosmoPulse - Multi-Planet Space Environment Tracking MVP

A unified platform that visualizes and tracks space objects, debris, and weather across multiple planets using NASA's open datasets.

## 🌟 Features

### Input Layer
- ✅ TLE (Two-Line Element) orbit data processing
- ✅ Radar tracking data (range, velocity, cross-section)
- ✅ Optical telescope observations
- ✅ NASA Space Weather integration
- ✅ Multi-sensor data fusion

### Processing Layer
- ✅ SGP4 orbit propagation engine
- ✅ Real-time position calculation
- ✅ Track association across time
- ✅ Object classification (satellites vs debris)
- ✅ Collision risk assessment
- ✅ Threat scoring algorithm

### Output Layer
- ✅ 3D orbital visualization (Earth & Mars)
- ✅ Ground track mapping
- ✅ Real-time alerts dashboard
- ✅ Risk heatmaps
- ✅ Mission impact reports
- ✅ Space weather monitoring
- ✅ Data catalog browser

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /Users/Ayan/Desktop/Hackathon
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run streamlit_app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Hackathon/
├── streamlit_app.py          # Main Streamlit dashboard
├── data_processor.py          # Data loading and processing
├── orbit_engine.py            # SGP4 orbit calculations
├── risk_assessment.py         # Collision risk algorithms
├── visualization.py           # Plotly 3D visualizations
├── requirements.txt           # Python dependencies
├── app.py                     # NASA data fetcher
├── mockdata.py               # Mock data generator
└── data/                     # Data directory
    ├── mock_tle.csv          # Satellite orbital elements
    ├── mock_radar.csv        # Radar tracking data
    ├── mock_optical.csv      # Telescope observations
    ├── mock_space_weather.csv # Space weather data
    └── ... (other data files)
```

## 🎯 Key Modules

### 1. Data Processor (`data_processor.py`)
- Loads TLE, radar, optical, and space weather data
- Parses orbital elements
- Merges multi-source data
- Classifies space objects

### 2. Orbit Engine (`orbit_engine.py`)
- SGP4 satellite propagation
- Trajectory generation
- Ground track calculation
- Keplerian element computation
- Mars orbit simulation

### 3. Risk Assessment (`risk_assessment.py`)
- Collision probability calculation
- Conjunction event detection
- Space weather impact analysis
- Threat level classification
- Mission impact scoring

### 4. Visualization (`visualization.py`)
- 3D orbital plots (Plotly)
- Ground track mapping
- Altitude profiles
- Risk heatmaps
- Space weather charts

## 📊 Dashboard Pages

### 🏠 Home
- System overview with key metrics
- Active alert summary
- Quick statistics
- Real-time status indicators

### 🌍 3D Visualization
- Interactive 3D orbital plots
- Multi-satellite trajectory view
- Ground track mapping
- Altitude profiles
- Risk distribution heatmap

### ⚠️ Alerts & Risks
- Real-time conjunction warnings
- Risk assessment dashboard
- Mission impact summary
- Detailed alert log
- Conjunction timeline

### 📊 Data Catalog
- Complete satellite catalog
- Radar tracking data browser
- Optical observation gallery
- Raw TLE data viewer
- CSV export functionality

### 🌤️ Space Weather
- Current conditions monitor
- Solar flare tracking
- Geomagnetic activity (Kp index)
- Solar wind speed trends
- Historical data analysis

### 📈 Mission Impact
- Executive summary report
- Risk breakdown analysis
- Top risk objects list
- Alert distribution charts
- Downloadable reports

## 🔬 Technical Details

### Orbit Propagation
- Uses SGP4 (Simplified General Perturbations) model
- Accurate for LEO, MEO, and GEO satellites
- Handles orbital perturbations
- Real-time position prediction

### Risk Calculation
Collision risk score based on:
- **Proximity Score (60%)**: Distance between objects
- **Velocity Score (30%)**: Relative velocity
- **Size Score (10%)**: Radar cross-section

Threat Levels:
- **CRITICAL**: < 2 km separation
- **HIGH**: 2-5 km separation
- **MEDIUM**: 5-10 km separation
- **LOW**: > 10 km separation

### Space Weather Impact
Factors considered:
- Solar flare class (A, B, C, M, X)
- Kp geomagnetic index (0-9)
- Solar wind speed
- Atmospheric density (drag effect)

## 📈 Data Sources

- **Mock TLE Data**: Simulated satellite orbital elements
- **NASA Space Weather**: Real-time solar activity
- **Radar Tracking**: Simulated range/velocity measurements
- **Optical Observations**: NASA image database
- **Space-Track.org**: Real TLE data (via `app.py`)

## 🎨 Customization

### Adjust Risk Thresholds
Edit `risk_assessment.py`:
```python
self.collision_threshold = 5.0  # km
self.critical_threshold = 2.0   # km
```

### Change Visualization Settings
Edit `visualization.py`:
```python
self.earth_radius = 6371.0  # km
resolution = 30  # sphere detail
```

### Modify Dashboard Layout
Edit `streamlit_app.py` to add/remove pages or customize UI.

## 🐛 Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Data Loading Issues
Ensure all CSV files exist in the `data/` directory. Run `mockdata.py` to regenerate:
```bash
cd data
python ../mockdata.py
```

## 🚀 Future Enhancements

- [ ] Real-time TLE updates via Space-Track API
- [ ] Machine learning for debris classification
- [ ] Multi-planet conjunction analysis
- [ ] Historical trajectory playback
- [ ] Mobile-responsive design
- [ ] WebGL-based 3D rendering for performance
- [ ] Automated report scheduling
- [ ] Email/SMS alert notifications

## 📝 License

MIT License - Feel free to use for hackathons, research, or commercial projects.

## 👥 Contributors

Built for NASA Space Apps Challenge 2024

## 🙏 Acknowledgments

- NASA Open Data Portal
- Space-Track.org
- SGP4 Library
- Plotly Visualization Library
- Streamlit Framework

---

**⭐ Star this repo if you find it useful!**

For questions or issues, please open a GitHub issue or contact the development team.
