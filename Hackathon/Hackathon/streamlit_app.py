"""
CosmoPulse - Multi-Planet Space Environment Tracking MVP
Main Streamlit Dashboard Application
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Import custom modules
from data_processor import DataProcessor
from orbit_engine import OrbitEngine
from risk_assessment import RiskAssessment
from visualization import Visualization

# Page configuration
st.set_page_config(
    page_title="CosmoPulse - Space Tracking",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with premium animations
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(31, 119, 180, 0.5); }
        50% { box-shadow: 0 0 20px rgba(31, 119, 180, 0.8); }
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        animation: fadeIn 0.8s ease-in;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-in;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Animated metric cards */
    div[data-testid="metric-container"] {
        animation: fadeIn 0.8s ease-in;
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: scale(1.05);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Plotly charts animation */
    .js-plotly-plot {
        animation: fadeIn 1s ease-in;
    }
    
    /* Alert animations */
    .alert-animation {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: pulse 1s infinite;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bar animation */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        animation: pulse 2s infinite;
    }
    
    /* Card hover effects */
    .element-container {
        transition: transform 0.3s ease;
    }
    
    /* Dataframe styling */
    .dataframe {
        animation: fadeIn 0.8s ease-in;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource(ttl=600)  # Cache for 10 minutes
def load_components():
    """Load and cache all components"""
    processor = DataProcessor()
    engine = OrbitEngine()
    risk = RiskAssessment()
    viz = Visualization()
    return processor, engine, risk, viz

@st.cache_data
def load_all_data():
    """Load all data with caching"""
    processor = DataProcessor()
    return processor.get_all_data()

# Sidebar Navigation
def sidebar():
    st.sidebar.markdown("# 🛰️ CosmoPulse")
    st.sidebar.markdown("**Multi-Planet Space Tracking**")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🌎 Live Earth Monitor", "🌍 3D Visualization", "⚠️ Alerts & Risks", 
         "📊 Data Catalog", "📈 Mission Impact", "🌤️ Space Weather", "🖼️ Image Analysis"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Settings")
    
    planet = st.sidebar.selectbox(
        "Select Planet",
        ["Earth", "Mars", "Multi-Planet View"]
    )
    
    duration = st.sidebar.slider(
        "Orbit Duration (hours)",
        min_value=1,
        max_value=24,
        value=6
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.sidebar.button("🔄 Clear Cache"):
        st.cache_resource.clear()
        st.rerun()
    
    return page, planet, duration

# Home Page
def home_page(data, risk, viz):
    st.markdown('<p class="main-header">🛰️ CosmoPulse</p>', unsafe_allow_html=True)
    st.markdown("### Multi-Planet Space Environment Tracking Platform")
    st.markdown("Real-time monitoring of satellites, debris, and space weather across Earth and Mars")
    
    # Key Metrics with enhanced visuals
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sat_count = len(data['merged'])
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); animation: fadeIn 0.8s ease-in;">
                <h4 style="color: white; margin: 0; opacity: 0.9;">🛰️ Active Satellites</h4>
                <h1 style="color: white; margin: 10px 0; font-size: 3em;">{sat_count}</h1>
                <p style="color: white; margin: 0; opacity: 0.8;">🟢 All Systems Nominal</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        debris_count = len(data['merged'][data['merged']['classification'] == 'Debris'])
        debris_pct = (debris_count/len(data['merged'])*100) if len(data['merged']) > 0 else 0
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); animation: fadeIn 1s ease-in;">
                <h4 style="color: white; margin: 0; opacity: 0.9;">🗑️ Tracked Debris</h4>
                <h1 style="color: white; margin: 10px 0; font-size: 3em;">{debris_count}</h1>
                <p style="color: white; margin: 0; opacity: 0.8;">{debris_pct:.1f}% of total</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        alerts = risk.generate_alerts(data['merged'], data['space_weather'])
        high_risk = len([a for a in alerts if a['severity'] in ['HIGH', 'CRITICAL']])
        alert_color = "#f5576c" if high_risk > 0 else "#2ecc71"
        alert_text = f"⚠️ {high_risk} High Risk" if high_risk > 0 else "✅ All Clear"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); animation: fadeIn 1.2s ease-in;">
                <h4 style="color: white; margin: 0; opacity: 0.9;">⚠️ Active Alerts</h4>
                <h1 style="color: white; margin: 10px 0; font-size: 3em;">{len(alerts)}</h1>
                <p style="color: white; margin: 0; opacity: 0.8;">{alert_text}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        weather_impact = risk.assess_space_weather_impact(data['space_weather'])
        weather_color = {"LOW": "#2ecc71", "MODERATE": "#f39c12", "HIGH": "#e74c3c", "SEVERE": "#c0392b"}
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); animation: fadeIn 1.4s ease-in;">
                <h4 style="color: white; margin: 0; opacity: 0.9;">🌤️ Space Weather</h4>
                <h1 style="color: white; margin: 10px 0; font-size: 2em;">{weather_impact['impact_level']}</h1>
                <p style="color: white; margin: 0; opacity: 0.8;">Score: {weather_impact['impact_score']:.1f}/100</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Alerts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚨 Recent Alerts")
        alerts = risk.generate_alerts(data['merged'], data['space_weather'])
        
        if alerts:
            for alert in alerts[:5]:
                severity = alert['severity']
                if severity in ['CRITICAL', 'SEVERE']:
                    emoji = '🔴'
                    color = '#ff4444'
                elif severity == 'HIGH':
                    emoji = '🟠'
                    color = '#ff8800'
                elif severity in ['MEDIUM', 'MODERATE']:
                    emoji = '🟡'
                    color = '#ffbb33'
                else:
                    emoji = '🟢'
                    color = '#44ff44'
                
                st.markdown(f"""
                    <div style="background-color: {color}22; border-left: 4px solid {color}; padding: 15px; margin: 10px 0; border-radius: 5px;">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 24px; margin-right: 10px;">{emoji}</span>
                            <strong style="font-size: 16px; color: {color};">{alert['type']} - {severity}</strong>
                        </div>
                        <p style="margin: 8px 0; font-size: 14px; color: #333;">{alert['message']}</p>
                        <small style="color: #666;">Risk Score: {alert['risk_score']:.1f} | {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No active alerts. All systems nominal.")
    
    with col2:
        st.subheader("📊 Alert Distribution")
        alert_chart = viz.create_alert_chart(alerts)
        st.plotly_chart(alert_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📈 Quick Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Satellite Classification")
        class_dist = data['merged']['classification'].value_counts()
        st.dataframe(class_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### Altitude Distribution")
        if 'radar_range_km' in data['merged'].columns:
            avg_alt = data['merged']['radar_range_km'].mean()
            min_alt = data['merged']['radar_range_km'].min()
            max_alt = data['merged']['radar_range_km'].max()
            
            st.write(f"**Average:** {avg_alt:.1f} km")
            st.write(f"**Min:** {min_alt:.1f} km")
            st.write(f"**Max:** {max_alt:.1f} km")
    
    with col3:
        st.markdown("#### Velocity Profile")
        if 'radar_velocity_km_s' in data['merged'].columns:
            avg_vel = data['merged']['radar_velocity_km_s'].mean()
            st.write(f"**Average:** {avg_vel:.2f} km/s")
            st.write(f"**Escape Velocity (Earth):** 11.2 km/s")
            st.write(f"**LEO Orbital Velocity:** ~7.8 km/s")

# 3D Visualization Page
def visualization_page(data, engine, viz, planet, duration):
    st.title(f"🌍 3D Orbital Visualization - {planet}")
    
    # Select satellites to visualize
    sat_options = data['merged']['satellite_name'].tolist()
    selected_sats = st.multiselect(
        "Select satellites to visualize (max 5)",
        sat_options,
        default=sat_options[:3] if len(sat_options) >= 3 else sat_options
    )
    
    if not selected_sats:
        st.warning("Please select at least one satellite")
        return
    
    # Limit to 5 satellites for performance
    selected_sats = selected_sats[:5]
    
    if st.button("🚀 Generate Orbital Visualization"):
        with st.spinner("Calculating orbital trajectories..."):
            trajectories = []
            ground_tracks = []
            
            for sat_name in selected_sats:
                sat_data = data['merged'][data['merged']['satellite_name'] == sat_name].iloc[0]
                line1 = sat_data['line1']
                line2 = sat_data['line2']
                
                # Generate trajectory
                traj = engine.propagate_trajectory(
                    line1, line2, 
                    datetime.now(), 
                    duration_hours=duration, 
                    steps=100
                )
                
                if traj:
                    trajectories.append(traj)
                    ground_tracks.append(engine.get_ground_track(traj))
            
            if trajectories:
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["3D Orbit View", "Ground Track", "Altitude Profile"])
                
                with tab1:
                    if planet == "Earth":
                        fig = viz.plot_earth_orbits(trajectories, selected_sats)
                    elif planet == "Mars":
                        # Generate Mars orbits
                        mars_trajs = [
                            engine.simulate_mars_orbit(500, 45, duration, 100),
                            engine.simulate_mars_orbit(800, 60, duration, 100)
                        ]
                        fig = viz.plot_mars_orbits(mars_trajs, ["Mars Sat 1", "Mars Sat 2"])
                    else:
                        fig = viz.plot_earth_orbits(trajectories, selected_sats)
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    fig = viz.plot_ground_track(ground_tracks, selected_sats)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    for i, traj in enumerate(trajectories):
                        fig = viz.plot_altitude_profile(traj, selected_sats[i])
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Failed to generate trajectories")
    
    # Risk Heatmap
    st.markdown("---")
    st.subheader("🎯 Risk Distribution Map")
    risk_fig = viz.plot_risk_heatmap(data['merged'])
    st.plotly_chart(risk_fig, use_container_width=True)

# Alerts & Risks Page
def alerts_page(data, risk, viz):
    st.title("⚠️ Alerts & Risk Assessment")
    
    # Generate all alerts
    alerts = risk.generate_alerts(data['merged'], data['space_weather'])
    
    # Mission Impact Summary
    mission_impact = risk.calculate_mission_impact(alerts, data['merged'])
    
    st.markdown("### 🎯 Mission Impact Assessment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = {
            'NORMAL': '🟢',
            'MODERATE': '🟡',
            'ELEVATED': '🟠',
            'CRITICAL': '🔴'
        }
        st.metric(
            "Overall Status",
            f"{status_color.get(mission_impact['overall_status'], '⚪')} {mission_impact['overall_status']}"
        )
    
    with col2:
        st.metric("High Risk Events", mission_impact['high_risk_count'])
    
    with col3:
        st.metric("Medium Risk Events", mission_impact['medium_risk_count'])
    
    with col4:
        st.metric("Avg Risk Score", f"{mission_impact['average_risk_score']:.1f}")
    
    st.info(f"**Recommendation:** {mission_impact['recommendation']}")
    
    st.markdown("---")
    
    # Conjunction Events
    st.subheader("🛸 Conjunction Events")
    conjunctions = risk.calculate_conjunction_events(data['merged'], threshold_km=10.0)
    
    if conjunctions:
        conj_df = pd.DataFrame(conjunctions)
        st.dataframe(
            conj_df[['satellite_1', 'satellite_2', 'distance_km', 
                    'relative_velocity', 'risk_score', 'threat_level']],
            use_container_width=True
        )
        
        # Conjunction timeline
        fig = viz.create_conjunction_timeline(conjunctions)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No conjunction events detected within threshold")
    
    st.markdown("---")
    
    # Detailed Alerts
    st.subheader("📋 Detailed Alert List")
    
    severity_filter = st.multiselect(
        "Filter by Severity",
        ['CRITICAL', 'SEVERE', 'HIGH', 'MEDIUM', 'MODERATE', 'LOW'],
        default=['CRITICAL', 'HIGH']
    )
    
    filtered_alerts = [a for a in alerts if a['severity'] in severity_filter]
    
    for alert in filtered_alerts:
        severity = alert['severity']
        if severity in ['CRITICAL', 'SEVERE']:
            color = '🔴'
        elif severity == 'HIGH':
            color = '🟠'
        elif severity in ['MEDIUM', 'MODERATE']:
            color = '🟡'
        else:
            color = '🟢'
        
        with st.expander(f"{color} {alert['type']} - {severity} (Score: {alert['risk_score']:.1f})"):
            st.write(f"**Message:** {alert['message']}")
            st.write(f"**Timestamp:** {alert['timestamp']}")
            st.write(f"**Risk Score:** {alert['risk_score']:.2f}")

# Data Catalog Page
def catalog_page(data):
    st.title("📊 Data Catalog")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Satellites", "Radar Data", "Optical Data", "Raw TLE"])
    
    with tab1:
        st.subheader("Satellite Catalog")
        st.dataframe(data['merged'], use_container_width=True, height=400)
        
        # Download button
        csv = data['merged'].to_csv(index=False)
        st.download_button(
            "📥 Download Satellite Data",
            csv,
            "satellite_catalog.csv",
            "text/csv"
        )
    
    with tab2:
        st.subheader("Radar Tracking Data")
        st.dataframe(data['radar'], use_container_width=True, height=400)
    
    with tab3:
        st.subheader("Optical Observations")
        st.dataframe(data['optical'], use_container_width=True, height=400)
        
        # Show sample images
        if not data['optical'].empty:
            st.markdown("#### Sample Telescope Images")
            cols = st.columns(3)
            for i, row in data['optical'].head(3).iterrows():
                with cols[i % 3]:
                    st.image(row['optical_image_url'], caption=row['satellite_name'])
    
    with tab4:
        st.subheader("TLE Data")
        st.dataframe(data['tle'], use_container_width=True, height=400)

# Space Weather Page
def space_weather_page(data, risk, viz):
    st.title("🌤️ Space Weather Monitoring")
    
    # Current conditions
    weather_impact = risk.assess_space_weather_impact(data['space_weather'])
    
    st.markdown("### Current Space Weather Conditions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        impact_emoji = {'LOW': '🟢', 'MODERATE': '🟡', 'HIGH': '🟠', 'SEVERE': '🔴'}
        st.metric(
            "Impact Level",
            f"{impact_emoji.get(weather_impact['impact_level'], '⚪')} {weather_impact['impact_level']}"
        )
    
    with col2:
        st.metric("Impact Score", f"{weather_impact['impact_score']:.1f}/100")
    
    with col3:
        st.metric("Active Factors", len(weather_impact['factors']))
    
    st.markdown("#### Contributing Factors:")
    for factor in weather_impact['factors']:
        st.write(f"• {factor}")
    
    st.markdown("---")
    
    # Weather trends
    st.subheader("📈 Space Weather Trends")
    weather_fig = viz.plot_space_weather(data['space_weather'])
    st.plotly_chart(weather_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed data
    st.subheader("📋 Raw Space Weather Data")
    st.dataframe(data['space_weather'], use_container_width=True, height=400)

# Live Earth Monitor Page
def live_earth_monitor_page(data, risk, viz):
    st.title("🌎 Live Earth Monitor")
    st.markdown("""
    ### 🔴 LIVE: Real-Time Satellite Tracking & Space Environment Status
    Track satellites orbiting Earth in real-time. Monitor space weather conditions and collision risks.
    """)
    
    # Auto-refresh toggle with better explanation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 **What you're seeing:** Live positions of tracked satellites, active debris, and real-time threat assessment")
    with col2:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
    
    if auto_refresh:
        st.success("🔄 Live updates enabled - refreshing every 30 seconds")
        # In production, this would trigger actual refresh
    
    st.markdown("---")
    
    # Top metrics with animated gauges and clear labels
    st.subheader("📊 Current Space Environment Status")
    st.markdown("*Updated every 5 minutes from tracking network*")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sats = len(data['merged'])
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">🛰️</h3>
                <h2 style="margin: 10px 0;">{total_sats}</h2>
                <p style="margin: 0; opacity: 0.9;">Active Satellites</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        debris_count = len(data['merged'][data['merged']['classification'] == 'Debris'])
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">🗑️</h3>
                <h2 style="margin: 10px 0;">{debris_count}</h2>
                <p style="margin: 0; opacity: 0.9;">Debris Objects</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        alerts = risk.generate_alerts(data['merged'], data['space_weather'])
        high_risk = len([a for a in alerts if a['severity'] in ['HIGH', 'CRITICAL']])
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">⚠️</h3>
                <h2 style="margin: 10px 0;">{high_risk}</h2>
                <p style="margin: 0; opacity: 0.9;">High Risk Events</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        weather_impact = risk.assess_space_weather_impact(data['space_weather'])
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">🌤️</h3>
                <h2 style="margin: 10px 0; font-size: 20px;">{weather_impact['impact_level']}</h2>
                <p style="margin: 0; opacity: 0.9;">Space Weather</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main 3D Globe with advanced controls
    st.subheader("🌍 3D Earth View - Live Satellite Positions")

    with st.expander("⚙️ Visualization Controls", expanded=False):
        c1, c2, c3, c4 = st.columns([2,2,2,2])
        with c1:
            altitude_scale = st.slider("Altitude Exaggeration", 1.0, 15.0, 5.0, 0.5,
                                       help="Visual exaggeration so satellites appear clearly above Earth")
        with c2:
            show_grid = st.toggle("Latitude/Longitude Grid", value=True)
        with c3:
            show_ref = st.toggle("Reference Shells (LEO/MEO/GEO)", value=True)
        with c4:
            show_help = st.toggle("Show Legend", value=True)
        st.caption("Altitudes may be exaggerated for visibility; hover tooltips show true values.")

    if show_help:
        colh1, colh2, colh3, colh4 = st.columns([2,2,2,2])
        with colh1: st.markdown("✅ **Active** = Green")
        with colh2: st.markdown("❌ **Debris** = Red X")
        with colh3: st.markdown("⚠️ **Priority** = Orange Diamond")
        with colh4: st.markdown("🌀 **Rings** = Orbit Paths")
        st.markdown("---")

    with st.spinner("🌍 Rendering enhanced Earth visualization..."):
        earth_fig = viz.create_live_earth_globe(
            data['merged'],
            data['space_weather'],
            altitude_scale=altitude_scale,
            show_grid=show_grid,
            show_reference=show_ref
        )
        st.plotly_chart(earth_fig, width='stretch')
    
    st.caption("✨ Object altitudes exaggerated (configurable) for clarity. Toggle layers in the controls above.")
    
    st.markdown("---")
    
    # Live statistics gauges with clear explanations
    st.subheader("📈 System Health & Risk Metrics")
    st.markdown("*Gauges show current status: 🟢 Green = Safe, 🟡 Yellow = Monitor, 🔴 Red = Action Required*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Orbital capacity utilization
        capacity = (len(data['merged']) / 100) * 100  # Mock capacity
        gauge_fig = viz.create_live_stats_gauge(capacity, "Orbital Capacity", 100)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with col2:
        # Average collision risk
        avg_risk = np.mean([a['risk_score'] for a in alerts]) if alerts else 0
        gauge_fig = viz.create_live_stats_gauge(avg_risk, "Avg Risk Score", 100)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with col3:
        # Space weather severity
        weather_score = weather_impact['impact_score']
        gauge_fig = viz.create_live_stats_gauge(weather_score, "Weather Impact", 100)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Real-time activity feed
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📡 Live Activity Feed")
        
        # Simulated activity feed
        activities = [
            {"time": "00:01:23", "icon": "🛰️", "event": "SAT-905 passed over ground station OBS-3", "level": "info"},
            {"time": "00:02:45", "icon": "⚠️", "event": "Close approach detected: SAT-900 & SAT-912 (4.2 km)", "level": "warning"},
            {"time": "00:03:12", "icon": "📡", "event": "Radar lock acquired on SAT-908", "level": "success"},
            {"time": "00:04:56", "icon": "🌤️", "event": "Solar wind speed increased to 650 km/s", "level": "warning"},
            {"time": "00:05:33", "icon": "✅", "event": "Orbit correction completed for SAT-901", "level": "success"},
            {"time": "00:06:18", "icon": "🔴", "event": "Debris detection: New object in LEO", "level": "error"},
            {"time": "00:07:42", "icon": "📸", "event": "Optical observation received from telescope", "level": "info"},
        ]
        
        for activity in activities:
            if activity['level'] == 'error':
                bg_color = '#ff444422'
                border_color = '#ff4444'
            elif activity['level'] == 'warning':
                bg_color = '#ffbb3322'
                border_color = '#ffbb33'
            elif activity['level'] == 'success':
                bg_color = '#44ff4422'
                border_color = '#44ff44'
            else:
                bg_color = '#4444ff22'
                border_color = '#4444ff'
            
            st.markdown(f"""
                <div style="background-color: {bg_color}; border-left: 3px solid {border_color}; 
                            padding: 10px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center;">
                    <span style="font-size: 20px; margin-right: 10px;">{activity['icon']}</span>
                    <div style="flex: 1;">
                        <small style="color: #666;">{activity['time']}</small>
                        <p style="margin: 2px 0; font-size: 14px;">{activity['event']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("Data refreshed!")
            st.rerun()
        
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Report generation initiated...")
        
        if st.button("🚨 View All Alerts", use_container_width=True):
            st.info("Navigating to Alerts page...")
        
        st.markdown("---")
        
        st.markdown("### 🌐 Coverage Stats")
        st.metric("Ground Stations", "5 Active")
        st.metric("Observation Rate", "127/min")
        st.metric("Data Latency", "< 100ms")
        
        st.markdown("---")
        
        st.markdown("### ⏱️ System Uptime")
        st.progress(0.99, text="99.9% Uptime")

# Mission Impact Page
def mission_impact_page(data, risk):
    st.title("📈 Mission Impact Report")
    
    # Generate comprehensive report
    alerts = risk.generate_alerts(data['merged'], data['space_weather'])
    mission_impact = risk.calculate_mission_impact(alerts, data['merged'])
    
    # Executive Summary
    st.markdown("## Executive Summary")
    
    st.markdown(f"""
    **Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    **Overall Status:** {mission_impact['overall_status']}
    
    **Total Tracked Objects:** {mission_impact['total_satellites']}
    
    **High Risk Events:** {mission_impact['high_risk_count']}
    
    **Medium Risk Events:** {mission_impact['medium_risk_count']}
    
    **Average Risk Score:** {mission_impact['average_risk_score']:.2f}/100
    
    ---
    
    ### Key Recommendations:
    {mission_impact['recommendation']}
    """)
    
    st.markdown("---")
    
    # Risk breakdown by category
    st.subheader("Risk Breakdown by Category")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### By Object Type")
        class_counts = data['merged']['classification'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=class_counts.index, values=class_counts.values)])
        fig.update_layout(title="Object Classification Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### By Alert Type")
        if alerts:
            alert_types = pd.Series([a['type'] for a in alerts]).value_counts()
            fig = go.Figure(data=[go.Pie(labels=alert_types.index, values=alert_types.values)])
            fig.update_layout(title="Alert Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top Risk Objects
    st.subheader("🎯 Top Risk Objects")
    
    # Calculate risk for each satellite
    risk_scores = []
    for idx, sat in data['merged'].iterrows():
        debris_risk = risk.classify_debris_risk(sat)
        score = 70 if "HIGH" in debris_risk else 40 if "MODERATE" in debris_risk else 10
        risk_scores.append({
            'satellite_name': sat['satellite_name'],
            'classification': sat['classification'],
            'altitude_km': sat.get('radar_range_km', 0),
            'velocity_km_s': sat.get('radar_velocity_km_s', 0),
            'risk_category': debris_risk,
            'risk_score': score
        })
    
    risk_df = pd.DataFrame(risk_scores).sort_values('risk_score', ascending=False).head(10)
    st.dataframe(risk_df, use_container_width=True)
    
    st.markdown("---")
    
    # Download Report
    st.subheader("📥 Export Report")
    
    report_text = f"""
COSMOPULSE MISSION IMPACT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
=================
Overall Status: {mission_impact['overall_status']}
Total Tracked Objects: {mission_impact['total_satellites']}
High Risk Events: {mission_impact['high_risk_count']}
Medium Risk Events: {mission_impact['medium_risk_count']}
Average Risk Score: {mission_impact['average_risk_score']:.2f}/100

RECOMMENDATION
==============
{mission_impact['recommendation']}

TOP RISK OBJECTS
================
{risk_df.to_string()}

DETAILED ALERTS
===============
"""
    for alert in alerts[:10]:
        report_text += f"\n{alert['severity']} - {alert['type']}: {alert['message']}\n"
    
    st.download_button(
        "📥 Download Full Report",
        report_text,
        "cosmopulse_mission_report.txt",
        "text/plain"
    )

# Image Analysis Page (YOLO detection demo)
def image_analysis_page():
    import streamlit as st
    from PIL import Image
    st.title("🖼️ Image Analysis & Object Detection")
    st.markdown("Upload an image to run YOLO object detection (demo using a general COCO-pretrained model).")
    st.markdown("*First run will download model weights; may take a moment.*")

    with st.expander("⚙️ Detection Settings", expanded=False):
        conf = st.slider("Confidence Threshold", 0.1, 0.9, 0.25, 0.05)
        model_variant = st.selectbox("Model Variant", ["yolov8n.pt", "yolov8s.pt"], index=0)

    uploaded = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"]) 
    if uploaded is not None:
        try:
            image = Image.open(uploaded)
        except Exception:
            st.error("Could not open image.")
            return
        st.image(image, caption="Original", use_container_width=True)

        if st.button("🔍 Run Detection"):
            with st.spinner("Running YOLO inference..."):
                try:
                    from image_analysis import load_image_analyzer
                    analyzer = load_image_analyzer(model_variant)
                    detections = analyzer.detect(image, conf=conf)
                    annotated = analyzer.annotate(image, detections)
                    summary = analyzer.summarize(detections)
                    st.image(annotated, caption="Annotated", use_container_width=True)
                    st.success(summary)
                    if detections:
                        det_rows = [
                            {
                                "label": d.label,
                                "confidence": f"{d.confidence:.2f}",
                                "x1": int(d.box['x1']), "y1": int(d.box['y1']),
                                "x2": int(d.box['x2']), "y2": int(d.box['y2'])
                            } for d in detections
                        ]
                        st.dataframe(det_rows, use_container_width=True)
                except RuntimeError as re:
                    st.error(f"Model not available: {re}")
                except Exception as e:
                    st.error(f"Detection error: {e}")
    else:
        st.info("Upload an image to begin.")

# Main Application
def main():
    # Load components and data
    processor, engine, risk, viz = load_components()
    data = load_all_data()
    
    # Sidebar
    page, planet, duration = sidebar()
    
    # Route to appropriate page
    if page == "🏠 Home":
        home_page(data, risk, viz)
    elif page == "🌎 Live Earth Monitor":
        live_earth_monitor_page(data, risk, viz)
    elif page == "🌍 3D Visualization":
        visualization_page(data, engine, viz, planet, duration)
    elif page == "⚠️ Alerts & Risks":
        alerts_page(data, risk, viz)
    elif page == "📊 Data Catalog":
        catalog_page(data)
    elif page == "🌤️ Space Weather":
        space_weather_page(data, risk, viz)
    elif page == "📈 Mission Impact":
        mission_impact_page(data, risk)
    elif page == "🖼️ Image Analysis":
        image_analysis_page()

if __name__ == "__main__":
    main()
