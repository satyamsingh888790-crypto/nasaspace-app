"""
CosmoPulse Orbit Propagation Engine
Uses SGP4 model for satellite orbit calculations
"""
from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
import numpy as np
from typing import Tuple, List, Dict
import math

class OrbitEngine:
    def __init__(self):
        self.earth_radius = 6371.0  # km
        self.mars_radius = 3389.5   # km
        
    def create_satellite(self, line1: str, line2: str) -> Satrec:
        """Create SGP4 satellite object from TLE"""
        try:
            satellite = Satrec.twoline2rv(line1, line2)
            return satellite
        except Exception as e:
            print(f"Error creating satellite: {e}")
            return None
    
    def propagate_orbit(self, satellite: Satrec, dt: datetime) -> Tuple[np.ndarray, np.ndarray]:
        """
        Propagate satellite position and velocity at given time
        Returns: (position [x,y,z] in km, velocity [vx,vy,vz] in km/s)
        """
        try:
            jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            e, r, v = satellite.sgp4(jd, fr)
            
            if e != 0:  # Error in propagation
                return None, None
            
            return np.array(r), np.array(v)
        except Exception as e:
            print(f"Error propagating orbit: {e}")
            return None, None
    
    def propagate_trajectory(self, line1: str, line2: str, 
                           start_time: datetime, 
                           duration_hours: float = 24, 
                           steps: int = 100) -> List[Dict]:
        """
        Generate full orbital trajectory over time
        """
        satellite = self.create_satellite(line1, line2)
        if not satellite:
            return []
        
        trajectory = []
        time_step = timedelta(hours=duration_hours / steps)
        
        for i in range(steps):
            current_time = start_time + i * time_step
            pos, vel = self.propagate_orbit(satellite, current_time)
            
            if pos is not None and vel is not None:
                trajectory.append({
                    'time': current_time,
                    'x': pos[0],
                    'y': pos[1],
                    'z': pos[2],
                    'vx': vel[0],
                    'vy': vel[1],
                    'vz': vel[2],
                    'altitude': np.linalg.norm(pos) - self.earth_radius,
                    'velocity_magnitude': np.linalg.norm(vel)
                })
        
        return trajectory
    
    def cartesian_to_spherical(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Convert Cartesian to Spherical coordinates"""
        r = math.sqrt(x**2 + y**2 + z**2)
        theta = math.acos(z / r) if r > 0 else 0  # Polar angle
        phi = math.atan2(y, x)  # Azimuthal angle
        return r, math.degrees(theta), math.degrees(phi)
    
    def calculate_orbital_elements(self, pos: np.ndarray, vel: np.ndarray) -> Dict:
        """
        Calculate Keplerian orbital elements from position and velocity
        """
        mu = 398600.4418  # Earth's gravitational parameter (km^3/s^2)
        
        r = np.linalg.norm(pos)
        v = np.linalg.norm(vel)
        
        # Specific orbital energy
        energy = (v**2 / 2) - (mu / r)
        
        # Semi-major axis
        a = -mu / (2 * energy) if energy != 0 else 0
        
        # Angular momentum vector
        h = np.cross(pos, vel)
        h_mag = np.linalg.norm(h)
        
        # Eccentricity vector
        e_vec = ((v**2 - mu/r) * pos - np.dot(pos, vel) * vel) / mu
        e = np.linalg.norm(e_vec)
        
        # Inclination
        i = math.acos(h[2] / h_mag) if h_mag > 0 else 0
        
        # Orbital period
        period = 2 * math.pi * math.sqrt(a**3 / mu) if a > 0 else 0
        
        return {
            'semi_major_axis_km': a,
            'eccentricity': e,
            'inclination_deg': math.degrees(i),
            'period_minutes': period / 60,
            'apogee_km': a * (1 + e) - self.earth_radius,
            'perigee_km': a * (1 - e) - self.earth_radius,
            'energy': energy,
            'angular_momentum': h_mag
        }
    
    def get_ground_track(self, trajectory: List[Dict]) -> List[Dict]:
        """
        Calculate ground track (latitude/longitude) from trajectory
        """
        ground_track = []
        
        for point in trajectory:
            x, y, z = point['x'], point['y'], point['z']
            
            # Convert to lat/lon
            lat = math.degrees(math.asin(z / math.sqrt(x**2 + y**2 + z**2)))
            lon = math.degrees(math.atan2(y, x))
            
            ground_track.append({
                'time': point['time'],
                'latitude': lat,
                'longitude': lon,
                'altitude': point['altitude']
            })
        
        return ground_track
    
    def simulate_mars_orbit(self, altitude_km: float, inclination_deg: float, 
                           duration_hours: float = 24, steps: int = 100) -> List[Dict]:
        """
        Simulate a simple circular orbit around Mars
        (Simplified model for MVP)
        """
        trajectory = []
        orbital_radius = self.mars_radius + altitude_km
        
        # Calculate orbital period using Kepler's third law
        mu_mars = 42828  # Mars gravitational parameter (km^3/s^2)
        period_seconds = 2 * math.pi * math.sqrt(orbital_radius**3 / mu_mars)
        angular_velocity = 2 * math.pi / period_seconds
        
        time_step = timedelta(hours=duration_hours / steps)
        start_time = datetime.now()
        
        for i in range(steps):
            current_time = start_time + i * time_step
            angle = angular_velocity * i * (duration_hours * 3600 / steps)
            
            # Simple circular orbit in inclined plane
            x = orbital_radius * math.cos(angle)
            y = orbital_radius * math.sin(angle) * math.cos(math.radians(inclination_deg))
            z = orbital_radius * math.sin(angle) * math.sin(math.radians(inclination_deg))
            
            trajectory.append({
                'time': current_time,
                'x': x,
                'y': y,
                'z': z,
                'altitude': altitude_km,
                'planet': 'Mars'
            })
        
        return trajectory
    
    def calculate_closest_approach(self, traj1: List[Dict], traj2: List[Dict]) -> Dict:
        """
        Calculate closest approach between two satellite trajectories
        """
        min_distance = float('inf')
        closest_time = None
        closest_points = None
        
        # Simple comparison (assumes synchronized timestamps)
        for p1, p2 in zip(traj1, traj2):
            pos1 = np.array([p1['x'], p1['y'], p1['z']])
            pos2 = np.array([p2['x'], p2['y'], p2['z']])
            
            distance = np.linalg.norm(pos1 - pos2)
            
            if distance < min_distance:
                min_distance = distance
                closest_time = p1['time']
                closest_points = (pos1, pos2)
        
        return {
            'min_distance_km': min_distance,
            'time': closest_time,
            'positions': closest_points
        }

if __name__ == "__main__":
    # Test the orbit engine
    engine = OrbitEngine()
    
    # Sample TLE
    line1 = "1 00900U 20001A   25276.94099447  .0000767  00000+0  12345-3 0  9997"
    line2 = "2 00900  47.0000  71.0000 667919 107.000  71.000 8.97609585 75649"
    
    trajectory = engine.propagate_trajectory(line1, line2, datetime.now(), duration_hours=2, steps=50)
    
    if trajectory:
        print(f"✅ Generated trajectory with {len(trajectory)} points")
        print(f"First position: x={trajectory[0]['x']:.2f}, y={trajectory[0]['y']:.2f}, z={trajectory[0]['z']:.2f}")
        print(f"Altitude: {trajectory[0]['altitude']:.2f} km")
