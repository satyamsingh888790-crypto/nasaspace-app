"""
CosmoPulse Visualization Module
3D orbital visualizations using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import List, Dict

class Visualization:
    def __init__(self):
        self.earth_radius = 6371.0  # km
        self.mars_radius = 3389.5   # km
        
    def create_sphere(self, radius: float, color: str, name: str, 
                     resolution: int = 30) -> go.Surface:
        """Create a sphere (planet) surface"""
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        return go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            name=name,
            hoverinfo='name'
        )
    
    def plot_earth_orbits(self, trajectories: List[Dict], 
                         satellite_names: List[str] = None) -> go.Figure:
        """
        Create 3D visualization of satellites orbiting Earth
        """
        fig = go.Figure()
        
        # Add Earth
        earth = self.create_sphere(self.earth_radius, '#1f77b4', 'Earth')
        fig.add_trace(earth)
        
        # Add satellite trajectories
        colors = px.colors.qualitative.Plotly
        
        for i, traj in enumerate(trajectories):
            if not traj:
                continue
                
            x_vals = [p['x'] for p in traj]
            y_vals = [p['y'] for p in traj]
            z_vals = [p['z'] for p in traj]
            
            name = satellite_names[i] if satellite_names and i < len(satellite_names) else f"Satellite {i+1}"
            color = colors[i % len(colors)]
            
            # Add trajectory line
            fig.add_trace(go.Scatter3d(
                x=x_vals, y=y_vals, z=z_vals,
                mode='lines',
                name=name,
                line=dict(color=color, width=2),
                hovertemplate=f'{name}<br>X: %{{x:.1f}} km<br>Y: %{{y:.1f}} km<br>Z: %{{z:.1f}} km'
            ))
            
            # Add current position marker
            fig.add_trace(go.Scatter3d(
                x=[x_vals[-1]], y=[y_vals[-1]], z=[z_vals[-1]],
                mode='markers',
                name=f'{name} (current)',
                marker=dict(size=8, color=color, symbol='diamond'),
                showlegend=False,
                hovertemplate=f'{name}<br>Current Position'
            ))
        
        # Update layout
        fig.update_layout(
            title='Earth Orbit Visualization - CosmoPulse',
            scene=dict(
                xaxis_title='X (km)',
                yaxis_title='Y (km)',
                zaxis_title='Z (km)',
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=700,
            showlegend=True,
            hovermode='closest'
        )
        
        return fig
    
    def plot_mars_orbits(self, trajectories: List[Dict], 
                        satellite_names: List[str] = None) -> go.Figure:
        """
        Create 3D visualization of satellites orbiting Mars
        """
        fig = go.Figure()
        
        # Add Mars
        mars = self.create_sphere(self.mars_radius, '#cd5c5c', 'Mars')
        fig.add_trace(mars)
        
        # Add satellite trajectories
        colors = px.colors.qualitative.Set2
        
        for i, traj in enumerate(trajectories):
            if not traj:
                continue
                
            x_vals = [p['x'] for p in traj]
            y_vals = [p['y'] for p in traj]
            z_vals = [p['z'] for p in traj]
            
            name = satellite_names[i] if satellite_names and i < len(satellite_names) else f"Mars Satellite {i+1}"
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter3d(
                x=x_vals, y=y_vals, z=z_vals,
                mode='lines+markers',
                name=name,
                line=dict(color=color, width=2),
                marker=dict(size=3, color=color)
            ))
        
        fig.update_layout(
            title='Mars Orbit Visualization - CosmoPulse',
            scene=dict(
                xaxis_title='X (km)',
                yaxis_title='Y (km)',
                zaxis_title='Z (km)',
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=700,
            showlegend=True
        )
        
        return fig
    
    def plot_ground_track(self, ground_tracks: List[Dict], 
                         satellite_names: List[str] = None) -> go.Figure:
        """
        Plot satellite ground tracks on 2D map projection
        """
        fig = go.Figure()
        
        colors = px.colors.qualitative.Plotly
        
        for i, track in enumerate(ground_tracks):
            if not track:
                continue
                
            lats = [p['latitude'] for p in track]
            lons = [p['longitude'] for p in track]
            
            name = satellite_names[i] if satellite_names and i < len(satellite_names) else f"Satellite {i+1}"
            
            fig.add_trace(go.Scattergeo(
                lat=lats,
                lon=lons,
                mode='lines+markers',
                name=name,
                line=dict(width=2, color=colors[i % len(colors)]),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title='Satellite Ground Tracks',
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
            ),
            height=500
        )
        
        return fig
    
    def plot_altitude_profile(self, trajectory: List[Dict], 
                             satellite_name: str = "Satellite") -> go.Figure:
        """
        Plot altitude over time
        """
        times = [p['time'] for p in trajectory]
        altitudes = [p['altitude'] for p in trajectory]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=times,
            y=altitudes,
            mode='lines',
            name='Altitude',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title=f'{satellite_name} - Altitude Profile',
            xaxis_title='Time',
            yaxis_title='Altitude (km)',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_risk_heatmap(self, satellites_data: pd.DataFrame) -> go.Figure:
        """
        Create heatmap of satellite risk levels
        """
        # Create risk matrix based on altitude and velocity
        if satellites_data.empty:
            return go.Figure()
        
        fig = px.scatter(
            satellites_data,
            x='radar_range_km',
            y='radar_velocity_km_s',
            size='radar_cross_section_m2',
            color='classification',
            hover_name='satellite_name',
            labels={
                'radar_range_km': 'Range (km)',
                'radar_velocity_km_s': 'Velocity (km/s)',
                'radar_cross_section_m2': 'RCS (m²)'
            },
            title='Satellite Risk Distribution'
        )
        
        fig.update_layout(height=500)
        
        return fig
    
    def plot_space_weather(self, weather_data: pd.DataFrame) -> go.Figure:
        """
        Visualize space weather trends
        """
        fig = go.Figure()
        
        if not weather_data.empty:
            # Solar wind speed
            fig.add_trace(go.Scatter(
                x=weather_data['timestamp'],
                y=weather_data['solar_wind_speed_km_s'],
                mode='lines',
                name='Solar Wind Speed',
                line=dict(color='orange', width=2),
                yaxis='y'
            ))
            
            # Kp index
            fig.add_trace(go.Scatter(
                x=weather_data['timestamp'],
                y=weather_data['kp_index'],
                mode='lines+markers',
                name='Kp Index',
                line=dict(color='red', width=2),
                yaxis='y2'
            ))
        
        fig.update_layout(
            title='Space Weather Conditions',
            xaxis_title='Time',
            yaxis=dict(title='Solar Wind Speed (km/s)', side='left'),
            yaxis2=dict(title='Kp Index', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_alert_chart(self, alerts: List[Dict]) -> go.Figure:
        """
        Create visualization of alerts by severity
        """
        if not alerts:
            return go.Figure()
        
        df = pd.DataFrame(alerts)
        severity_counts = df['severity'].value_counts()
        
        colors = {
            'CRITICAL': '#d62728',
            'HIGH': '#ff7f0e',
            'MEDIUM': '#ffbb33',
            'MODERATE': '#ffbb33',
            'SEVERE': '#d62728',
            'LOW': '#2ca02c'
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=severity_counts.index,
                y=severity_counts.values,
                marker_color=[colors.get(x, '#1f77b4') for x in severity_counts.index],
                text=severity_counts.values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title='Alerts by Severity Level',
            xaxis_title='Severity',
            yaxis_title='Count',
            height=400
        )
        
        return fig
    
    def create_conjunction_timeline(self, conjunctions: List[Dict]) -> go.Figure:
        """
        Timeline of predicted conjunction events
        """
        if not conjunctions:
            return go.Figure()
        
        df = pd.DataFrame(conjunctions)
        
        fig = px.scatter(
            df,
            x='timestamp',
            y='distance_km',
            color='threat_level',
            size='risk_score',
            hover_data=['satellite_1', 'satellite_2'],
            title='Conjunction Events Timeline',
            labels={'distance_km': 'Distance (km)', 'timestamp': 'Time'},
            color_discrete_map={
                'CRITICAL': '#d62728',
                'HIGH': '#ff7f0e',
                'MEDIUM': '#ffbb33',
                'LOW': '#2ca02c'
            }
        )
        
        fig.add_hline(y=5, line_dash="dash", line_color="red", 
                     annotation_text="Collision Threshold")
        
        fig.update_layout(height=400)
        
        return fig

    def _generate_continent_mask(self, lat_grid: np.ndarray, lon_grid: np.ndarray) -> np.ndarray:
        """Generate a deterministic pseudo-continent mask (0=water,1=land)."""
        # Combine several low-frequency trig components for large shapes
        mask = (
            0.55 * (np.sin(1.3 * lat_grid) * np.cos(0.9 * lon_grid)) +
            0.25 * (np.sin(2.1 * lat_grid + 0.5) * np.cos(1.7 * lon_grid - 0.3)) +
            0.15 * np.sin(3.5 * lon_grid + 1.2) * np.cos(0.6 * lat_grid) +
            0.10 * np.sin(4.2 * lat_grid - lon_grid)
        )
        # Normalize to 0..1
        mask = (mask - mask.min()) / (mask.max() - mask.min())
        # Sharpen land edges
        mask = np.power(mask, 1.4)
        # Threshold to create land vs water with gradient shores
        return mask

    def _land_elevation(self, mask: np.ndarray) -> np.ndarray:
        """Create elevation-ish relief based on land mask (0..1)."""
        # Add small scale perturbations for texture
        noise = 0.15 * np.sin(8 * mask) + 0.05 * np.cos(14 * mask)
        elev = mask + noise
        elev = (elev - elev.min()) / (elev.max() - elev.min())
        return elev

    def _build_color_scale(self) -> list:
        return [
            [0.00, '#001a33'],  # Deep ocean
            [0.08, '#003d66'],  # Mid ocean
            [0.16, '#005c99'],  # Shallow ocean
            [0.24, '#0077b8'],  # Coastal water
            [0.28, '#c2b280'],  # Beaches (sand)
            [0.34, '#a3d977'],  # Low plains
            [0.42, '#4caf50'],  # Vegetation
            [0.52, '#2e7d32'],  # Dense forest
            [0.62, '#6e4b2a'],  # Highlands
            [0.74, '#8d5e34'],  # Mountains lower
            [0.85, '#bfa17a'],  # Mountains higher
            [0.93, '#d9d9d9'],  # Snow transition
            [1.00, '#ffffff'],  # Ice / poles
        ]

    def create_live_earth_globe(self, satellites_data: pd.DataFrame,
                                 space_weather: pd.DataFrame,
                                 altitude_scale: float = 1.0,
                                 show_grid: bool = True,
                                 show_reference: bool = True) -> go.Figure:
        """Render an Earth globe with improved realism.

        Parameters
        ----------
        satellites_data : DataFrame
            Satellite catalog including altitude (radar_range_km or derived).
        space_weather : DataFrame
            For optional aurora effects.
        altitude_scale : float
            Exaggeration factor for altitude visualization (e.g. 5 makes satellites further out).
        show_grid : bool
            Show latitude / longitude grid lines.
        show_reference : bool
            Show LEO/GEO reference shells.
        """
        fig = go.Figure()

        # Sphere resolution (balanced)
        lat_res = 90
        lon_res = 180
        lat = np.linspace(-np.pi/2, np.pi/2, lat_res)
        lon = np.linspace(-np.pi, np.pi, lon_res)
        lon_grid, lat_grid = np.meshgrid(lon, lat)

        # Cartesian coordinates
        R = self.earth_radius
        x = R * np.cos(lat_grid) * np.cos(lon_grid)
        y = R * np.cos(lat_grid) * np.sin(lon_grid)
        z = R * np.sin(lat_grid)

        # Land / water & elevation
        mask = self._generate_continent_mask(lat_grid, lon_grid)
        elevation = self._land_elevation(mask)
        surface = elevation

        # Apply polar ice caps
        polar_band = (np.abs(lat_grid) > np.deg2rad(70))
        surface = np.where(polar_band, 1.0, surface)

        # Add Earth surface
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=surface,
            colorscale=self._build_color_scale(),
            showscale=False,
            name='Earth',
            hoverinfo='skip',
            opacity=1.0,
            lighting=dict(
                ambient=0.55,
                diffuse=0.85,
                specular=0.25,
                roughness=0.45,
                fresnel=0.18
            ),
            lightposition=dict(x=18000, y=12000, z=10000),
            hidesurface=False
        ))

        # Grid lines
        if show_grid:
            grid_lats = range(-60, 61, 30)
            grid_lons = range(-150, 181, 30)
            for glat in grid_lats:
                glat_rad = np.deg2rad(glat)
                lon_line = np.linspace(-np.pi, np.pi, 200)
                xg = R * np.cos(glat_rad) * np.cos(lon_line)
                yg = R * np.cos(glat_rad) * np.sin(lon_line)
                zg = R * np.sin(glat_rad) * np.ones_like(lon_line)
                fig.add_trace(go.Scatter3d(
                    x=xg, y=yg, z=zg,
                    mode='lines',
                    line=dict(color='rgba(255,255,255,0.15)', width=1),
                    hoverinfo='skip', showlegend=False
                ))
            for glon in grid_lons:
                glon_rad = np.deg2rad(glon)
                lat_line = np.linspace(-np.pi/2, np.pi/2, 200)
                xg = R * np.cos(lat_line) * np.cos(glon_rad)
                yg = R * np.cos(lat_line) * np.sin(glon_rad)
                zg = R * np.sin(lat_line)
                fig.add_trace(go.Scatter3d(
                    x=xg, y=yg, z=zg,
                    mode='lines',
                    line=dict(color='rgba(255,255,255,0.10)', width=1),
                    hoverinfo='skip', showlegend=False
                ))
        
        # Satellites with altitude exaggeration
        if not satellites_data.empty:
            alt_col = None
            for candidate in ['radar_range_km', 'altitude_km', 'alt_km']:
                if candidate in satellites_data.columns:
                    alt_col = candidate
                    break
            # If no altitude column, synthesize average 550 km
            if alt_col is None:
                satellites_data = satellites_data.copy()
                satellites_data['altitude_km'] = 550
                alt_col = 'altitude_km'

            np.random.seed(2025)
            shown_legends = set()
            max_display = 25
            subset = satellites_data.head(max_display)
            for idx, (_, sat) in enumerate(subset.iterrows()):
                base_alt = float(sat.get(alt_col, 550))
                base_alt = max(base_alt, 160)  # Minimum realistic LEO
                vis_alt = base_alt * altitude_scale
                r_orbit = R + vis_alt
                # Choose reproducible angles based on index
                theta = (idx * 137.5) % 360  # golden angle distribution
                phi = 25 + (idx * 47) % 130  # avoid poles (deg)
                theta_rad = np.deg2rad(theta)
                phi_rad = np.deg2rad(phi)
                # Convert
                sat_x = r_orbit * np.sin(phi_rad) * np.cos(theta_rad)
                sat_y = r_orbit * np.sin(phi_rad) * np.sin(theta_rad)
                sat_z = r_orbit * np.cos(phi_rad)

                classification = sat.get('classification', 'Satellite')
                if 'Debris' in classification:
                    color = '#ff1744'; symbol = 'x'; size = 9; group = '❌ Debris'
                elif any(k in classification for k in ['High','Priority']):
                    color = '#ffa726'; symbol = 'diamond'; size = 11; group = '⚠️ High Priority'
                else:
                    color = '#00e676'; symbol = 'circle'; size = 9; group = '✅ Active'

                show_legend = group not in shown_legends
                if show_legend: shown_legends.add(group)

                fig.add_trace(go.Scatter3d(
                    x=[sat_x], y=[sat_y], z=[sat_z],
                    mode='markers',
                    name=group,
                    legendgroup=group,
                    showlegend=show_legend,
                    marker=dict(size=size, color=color, symbol=symbol, line=dict(color='white', width=1)),
                    hovertemplate=(
                        f"<b>{sat.get('satellite_name','Object')}</b><br>"+
                        f"True Altitude: {base_alt:.0f} km<br>"+
                        ("Exaggerated Display Altitude: %.0f km<br>" % vis_alt if altitude_scale!=1 else "")+
                        f"Classification: {classification}<br><extra></extra>"
                    )
                ))

                # Orbit ring (display) for first 6
                if idx < 6:
                    ring_theta = np.linspace(0, 2*np.pi, 120)
                    ring_phi = phi_rad
                    rx = r_orbit * np.sin(ring_phi) * np.cos(ring_theta)
                    ry = r_orbit * np.sin(ring_phi) * np.sin(ring_theta)
                    rz = r_orbit * np.full_like(ring_theta, np.cos(ring_phi))
                    fig.add_trace(go.Scatter3d(
                        x=rx, y=ry, z=rz,
                        mode='lines',
                        line=dict(color=color, width=1, dash='dot'),
                        opacity=0.25,
                        hoverinfo='skip',
                        showlegend=False
                    ))
        
        if show_reference:
            # LEO shell
            for alt, label, col in [(500, 'LEO ~500 km', 'rgba(80,160,255,0.07)'),
                                    (2000, 'MEO ~2000 km', 'rgba(255,200,80,0.05)'),
                                    (35786, 'GEO ~35786 km', 'rgba(150,255,150,0.04)')]:
                # Skip GEO if altitude_scale small (would be huge). Display if scale <=5 with surface ring.
                if alt > 5000 and altitude_scale > 3:
                    continue
                shell_r = R + alt * altitude_scale
                u_s = np.linspace(0, 2*np.pi, 48)
                v_s = np.linspace(0, np.pi, 24)
                xs = shell_r * np.outer(np.cos(u_s), np.sin(v_s))
                ys = shell_r * np.outer(np.sin(u_s), np.sin(v_s))
                zs = shell_r * np.outer(np.ones_like(u_s), np.cos(v_s))
                fig.add_trace(go.Surface(
                    x=xs, y=ys, z=zs,
                    surfacecolor=np.zeros((len(u_s), len(v_s))),
                    colorscale=[[0, col],[1,col]],
                    showscale=False,
                    opacity=0.15 if alt<600 else 0.08,
                    name=label,
                    hoverinfo='text',
                    text=label,
                    lighting=dict(ambient=1, diffuse=0, specular=0),
                    # showsurface removed (invalid prop) – default behavior keeps surface visible
                ))
        
        # Add simplified background stars (small and subtle)
        np.random.seed(42)
        n_stars = 150
        star_distance = self.earth_radius * 10
        
        star_theta = np.random.uniform(0, 2*np.pi, n_stars)
        star_phi = np.random.uniform(0, np.pi, n_stars)
        
        star_x = star_distance * np.sin(star_phi) * np.cos(star_theta)
        star_y = star_distance * np.sin(star_phi) * np.sin(star_theta)
        star_z = star_distance * np.cos(star_phi)
        
        fig.add_trace(go.Scatter3d(
            x=star_x, y=star_y, z=star_z,
            mode='markers',
            name='Stars',
            marker=dict(
                size=1,
                color='white',
                opacity=0.5
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # NO ATMOSPHERE LAYER - keeping Earth solid and clear
        
        # Optional: Add simple aurora rings if space weather is active
        if not space_weather.empty:
            latest_weather = space_weather.iloc[-1]
            kp_index = latest_weather.get('kp_index', 3)
            
            if kp_index > 5:
                theta_aurora = np.linspace(0, 2*np.pi, 50)
                r_aurora = self.earth_radius * 1.01
                
                # Simple aurora ring at north pole
                x_aurora = r_aurora * np.cos(theta_aurora)
                y_aurora = r_aurora * np.sin(theta_aurora)
                z_aurora = np.full_like(theta_aurora, self.earth_radius * 0.9)
                
                fig.add_trace(go.Scatter3d(
                    x=x_aurora, y=y_aurora, z=z_aurora,
                    mode='lines',
                    name='Aurora',
                    line=dict(color='#00ff88', width=3),
                    hoverinfo='skip',
                    showlegend=False
                ))
        
        # Altitude scaling annotation
        scale_note = f"Altitude Exaggeration: {altitude_scale}x" if altitude_scale != 1 else "True Scale Altitudes"

        fig.update_layout(
            title=dict(
                text=f'<b>🌍 LIVE EARTH MONITOR</b><br><sub style="font-size: 13px;">Interactive 3D Globe | {scale_note}</sub>',
                font=dict(size=22, color='#ffffff'),
                x=0.5,
                xanchor='center',
                y=0.97,
                yanchor='top'
            ),
            scene=dict(
                xaxis=dict(
                    visible=False,
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False,
                    showbackground=False,
                    showspikes=False
                ),
                yaxis=dict(
                    visible=False,
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False,
                    showbackground=False,
                    showspikes=False
                ),
                zaxis=dict(
                    visible=False,
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False,
                    showbackground=False,
                    showspikes=False
                ),
                aspectmode='data',
                aspectratio=dict(x=1, y=1, z=1),
                camera=dict(
                    eye=dict(x=2.2, y=2.2, z=1.8),  # Better viewing distance
                    center=dict(x=0, y=0, z=0),
                    up=dict(x=0, y=0, z=1)
                ),
                bgcolor='#000814',  # Dark space background
                dragmode='orbit'  # Enable orbital rotation
            ),
            paper_bgcolor='#0a1128',
            plot_bgcolor='#000814',
            height=650,
            showlegend=True,
            legend=dict(
                bgcolor='rgba(15, 23, 42, 0.95)',
                font=dict(color='#ffffff', size=11),
                bordercolor='rgba(59, 130, 246, 0.6)',
                borderwidth=1,
                x=0.02,
                y=0.98,
                xanchor='left',
                yanchor='top',
                title=dict(
                    text='<b>📡 OBJECTS</b>',
                    font=dict(size=12, color='#60a5fa')
                )
            ),
            hovermode='closest',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=70, b=10)
        )
        
        # Add annotation for scaling explanation
        if altitude_scale != 1:
            fig.add_annotation(
                text="Satellite altitudes visually exaggerated for clarity",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.01, y=0.02,
                font=dict(size=11, color='#bbbbbb')
            )

        return fig
    
    def create_live_stats_gauge(self, value: float, title: str, 
                               max_value: float = 100) -> go.Figure:
        """
        Create animated gauge chart for live statistics
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 20}},
            delta={'reference': max_value * 0.7},
            gauge={
                'axis': {'range': [None, max_value], 'tickwidth': 1},
                'bar': {'color': "#1f77b4"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, max_value*0.33], 'color': '#d4edda'},
                    {'range': [max_value*0.33, max_value*0.66], 'color': '#fff3cd'},
                    {'range': [max_value*0.66, max_value], 'color': '#f8d7da'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig

if __name__ == "__main__":
    print("✅ Visualization module loaded")
