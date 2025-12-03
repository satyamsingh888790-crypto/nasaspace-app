"""
CosmoPulse Data Processor
Loads and processes satellite data from various sources
"""
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Tuple

class DataProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
    def load_tle_data(self, filename: str = "mock_tle.csv") -> pd.DataFrame:
        """Load Two-Line Element (TLE) orbital data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading TLE data: {e}")
            return pd.DataFrame()
    
    def load_radar_data(self, filename: str = "mock_radar.csv") -> pd.DataFrame:
        """Load radar tracking data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading radar data: {e}")
            return pd.DataFrame()
    
    def load_optical_data(self, filename: str = "mock_optical.csv") -> pd.DataFrame:
        """Load optical telescope observation data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading optical data: {e}")
            return pd.DataFrame()
    
    def load_space_weather(self, filename: str = "mock_space_weather.csv") -> pd.DataFrame:
        """Load space weather data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading space weather data: {e}")
            return pd.DataFrame()
    
    def load_observer_data(self, filename: str = "mock_observer.csv") -> pd.DataFrame:
        """Load ground observer station data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading observer data: {e}")
            return pd.DataFrame()
    
    def load_lightcurve_data(self, filename: str = "mock_lightcurve.csv") -> pd.DataFrame:
        """Load satellite brightness and rotation data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading lightcurve data: {e}")
            return pd.DataFrame()
    
    def load_spectral_data(self, filename: str = "mock_spectral.csv") -> pd.DataFrame:
        """Load spectral analysis data"""
        try:
            path = os.path.join(self.data_dir, filename)
            df = pd.read_csv(path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"Error loading spectral data: {e}")
            return pd.DataFrame()
    
    def parse_tle_lines(self, line1: str, line2: str) -> Dict:
        """Parse TLE orbital parameters"""
        try:
            # Extract key orbital elements from TLE
            inclination = float(line2[8:16].strip())
            raan = float(line2[17:25].strip())  # Right Ascension of Ascending Node
            eccentricity = float("0." + line2[26:33].strip())
            arg_perigee = float(line2[34:42].strip())
            mean_anomaly = float(line2[43:51].strip())
            mean_motion = float(line2[52:63].strip())
            
            return {
                'inclination': inclination,
                'raan': raan,
                'eccentricity': eccentricity,
                'arg_perigee': arg_perigee,
                'mean_anomaly': mean_anomaly,
                'mean_motion': mean_motion,
                'period_minutes': 1440.0 / mean_motion if mean_motion > 0 else 0
            }
        except Exception as e:
            print(f"Error parsing TLE: {e}")
            return {}
    
    def merge_satellite_data(self) -> pd.DataFrame:
        """Merge all satellite data sources into unified dataset"""
        tle_df = self.load_tle_data()
        radar_df = self.load_radar_data()
        optical_df = self.load_optical_data()
        
        # Merge on norad_id
        merged = tle_df.merge(
            radar_df[['norad_id', 'radar_range_km', 'radar_velocity_km_s', 'radar_cross_section_m2']], 
            on='norad_id', 
            how='left'
        )
        
        merged = merged.merge(
            optical_df[['norad_id', 'optical_image_url', 'observer_lat', 'observer_lon']], 
            on='norad_id', 
            how='left'
        )
        
        # Add parsed TLE parameters
        merged['orbital_params'] = merged.apply(
            lambda row: self.parse_tle_lines(row['line1'], row['line2']), 
            axis=1
        )
        
        return merged
    
    def classify_objects(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """Classify space objects based on characteristics"""
        def classify(row):
            if pd.isna(row['radar_cross_section_m2']):
                return 'Unknown'
            
            rcs = row['radar_cross_section_m2']
            altitude = row['radar_range_km']
            
            # Simple classification logic
            if rcs < 0.02:
                return 'Debris'
            elif altitude > 1000:
                return 'Satellite (High Orbit)'
            elif altitude > 500:
                return 'Satellite (Medium Orbit)'
            else:
                return 'Satellite (Low Orbit)'
        
        merged_df['classification'] = merged_df.apply(classify, axis=1)
        return merged_df
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all available data sources"""
        return {
            'tle': self.load_tle_data(),
            'radar': self.load_radar_data(),
            'optical': self.load_optical_data(),
            'space_weather': self.load_space_weather(),
            'observer': self.load_observer_data(),
            'lightcurve': self.load_lightcurve_data(),
            'spectral': self.load_spectral_data(),
            'merged': self.classify_objects(self.merge_satellite_data())
        }

if __name__ == "__main__":
    processor = DataProcessor()
    data = processor.get_all_data()
    print("✅ Data loaded successfully!")
    print(f"TLE records: {len(data['tle'])}")
    print(f"Radar records: {len(data['radar'])}")
    print(f"Merged records: {len(data['merged'])}")
