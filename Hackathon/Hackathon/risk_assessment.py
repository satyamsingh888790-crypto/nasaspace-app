"""
CosmoPulse Risk Assessment Module
Calculates collision probabilities and threat levels
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import math

class RiskAssessment:
    def __init__(self):
        # Collision threshold (km)
        self.collision_threshold = 5.0  # 5km safety zone
        self.critical_threshold = 2.0   # 2km critical zone
        self.warning_threshold = 10.0   # 10km warning zone
        
    def calculate_collision_risk(self, distance_km: float, relative_velocity_km_s: float,
                                 rcs1: float = 0.05, rcs2: float = 0.05) -> Dict:
        """
        Calculate collision risk based on distance and relative velocity
        Returns risk score (0-100) and threat level
        """
        # Proximity score (closer = higher risk)
        if distance_km <= self.critical_threshold:
            proximity_score = 100
            threat_level = "CRITICAL"
        elif distance_km <= self.collision_threshold:
            proximity_score = 80
            threat_level = "HIGH"
        elif distance_km <= self.warning_threshold:
            proximity_score = 50 * (1 - (distance_km - self.collision_threshold) / 
                                   (self.warning_threshold - self.collision_threshold))
            threat_level = "MEDIUM"
        else:
            proximity_score = 20 * math.exp(-(distance_km - self.warning_threshold) / 10)
            threat_level = "LOW"
        
        # Velocity score (higher relative velocity = higher risk)
        velocity_score = min(100, relative_velocity_km_s * 10)
        
        # Size/RCS score (larger objects = higher risk)
        size_score = min(100, (rcs1 + rcs2) * 500)
        
        # Combined risk score (weighted average)
        risk_score = (proximity_score * 0.6 + velocity_score * 0.3 + size_score * 0.1)
        
        return {
            'risk_score': round(risk_score, 2),
            'threat_level': threat_level,
            'distance_km': distance_km,
            'relative_velocity': relative_velocity_km_s,
            'proximity_score': round(proximity_score, 2),
            'velocity_score': round(velocity_score, 2),
            'size_score': round(size_score, 2)
        }
    
    def assess_space_weather_impact(self, weather_data: pd.DataFrame) -> Dict:
        """
        Assess impact of space weather on satellite operations
        """
        if weather_data.empty:
            return {'impact': 'UNKNOWN', 'score': 0}
        
        latest = weather_data.iloc[-1]
        
        impact_score = 0
        factors = []
        
        # Solar flare impact
        flare_class = latest.get('solar_flare_class', 'A')
        flare_scores = {'A': 10, 'B': 25, 'C': 50, 'M': 75, 'X': 100}
        flare_impact = flare_scores.get(flare_class, 10)
        impact_score += flare_impact * 0.4
        factors.append(f"Solar Flare: {flare_class}-class")
        
        # Kp index (geomagnetic activity)
        kp_index = latest.get('kp_index', 0)
        kp_impact = min(100, kp_index * 11)
        impact_score += kp_impact * 0.3
        factors.append(f"Kp Index: {kp_index}")
        
        # Solar wind speed
        solar_wind = latest.get('solar_wind_speed_km_s', 400)
        wind_impact = max(0, min(100, (solar_wind - 300) / 5))
        impact_score += wind_impact * 0.2
        factors.append(f"Solar Wind: {solar_wind:.1f} km/s")
        
        # Atmospheric density (drag effect)
        density = latest.get('atmospheric_density', 0)
        density_impact = min(100, density * 1e11)
        impact_score += density_impact * 0.1
        
        # Determine impact level
        if impact_score >= 75:
            impact_level = "SEVERE"
        elif impact_score >= 50:
            impact_level = "HIGH"
        elif impact_score >= 25:
            impact_level = "MODERATE"
        else:
            impact_level = "LOW"
        
        return {
            'impact_level': impact_level,
            'impact_score': round(impact_score, 2),
            'factors': factors,
            'timestamp': latest.get('timestamp')
        }
    
    def calculate_conjunction_events(self, satellites_data: pd.DataFrame, 
                                    threshold_km: float = 10.0) -> List[Dict]:
        """
        Identify potential conjunction events (close approaches) between satellites
        """
        conjunctions = []
        
        # Compare each pair of satellites
        for i in range(len(satellites_data)):
            for j in range(i + 1, len(satellites_data)):
                sat1 = satellites_data.iloc[i]
                sat2 = satellites_data.iloc[j]
                
                # Use radar range as proxy for position (simplified)
                if 'radar_range_km' in sat1 and 'radar_range_km' in sat2:
                    # Simplified distance calculation
                    distance = abs(sat1['radar_range_km'] - sat2['radar_range_km'])
                    
                    if distance < threshold_km:
                        rel_velocity = abs(sat1.get('radar_velocity_km_s', 7.5) - 
                                         sat2.get('radar_velocity_km_s', 7.5))
                        
                        risk = self.calculate_collision_risk(
                            distance, 
                            rel_velocity,
                            sat1.get('radar_cross_section_m2', 0.05),
                            sat2.get('radar_cross_section_m2', 0.05)
                        )
                        
                        conjunctions.append({
                            'satellite_1': sat1.get('satellite_name', f"SAT-{i}"),
                            'satellite_2': sat2.get('satellite_name', f"SAT-{j}"),
                            'norad_1': sat1.get('norad_id'),
                            'norad_2': sat2.get('norad_id'),
                            'distance_km': distance,
                            'relative_velocity': rel_velocity,
                            'risk_score': risk['risk_score'],
                            'threat_level': risk['threat_level'],
                            'timestamp': datetime.now()
                        })
        
        # Sort by risk score (descending)
        conjunctions.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return conjunctions
    
    def classify_debris_risk(self, object_data: pd.Series) -> str:
        """
        Classify debris risk level based on characteristics
        """
        rcs = object_data.get('radar_cross_section_m2', 0)
        altitude = object_data.get('radar_range_km', 0)
        velocity = object_data.get('radar_velocity_km_s', 0)
        
        risk_factors = 0
        
        # Small RCS (debris-like)
        if rcs < 0.02:
            risk_factors += 2
        
        # Critical altitude zones (LEO congestion)
        if 400 <= altitude <= 600 or 800 <= altitude <= 1000:
            risk_factors += 2
        
        # High velocity
        if velocity > 7.8:
            risk_factors += 1
        
        if risk_factors >= 4:
            return "HIGH DEBRIS RISK"
        elif risk_factors >= 2:
            return "MODERATE DEBRIS RISK"
        else:
            return "LOW DEBRIS RISK"
    
    def generate_alerts(self, satellites_data: pd.DataFrame, 
                       space_weather: pd.DataFrame) -> List[Dict]:
        """
        Generate prioritized alerts for all threats
        """
        alerts = []
        
        # Check conjunctions
        conjunctions = self.calculate_conjunction_events(satellites_data)
        for conj in conjunctions[:5]:  # Top 5 conjunction risks
            if conj['risk_score'] > 50:
                alerts.append({
                    'type': 'CONJUNCTION',
                    'severity': conj['threat_level'],
                    'message': f"Close approach: {conj['satellite_1']} & {conj['satellite_2']} ({conj['distance_km']:.2f} km)",
                    'risk_score': conj['risk_score'],
                    'timestamp': conj['timestamp']
                })
        
        # Check space weather
        weather_impact = self.assess_space_weather_impact(space_weather)
        if weather_impact['impact_score'] > 50:
            alerts.append({
                'type': 'SPACE WEATHER',
                'severity': weather_impact['impact_level'],
                'message': f"Elevated space weather activity: {', '.join(weather_impact['factors'])}",
                'risk_score': weather_impact['impact_score'],
                'timestamp': weather_impact.get('timestamp', datetime.now())
            })
        
        # Check debris risks
        for idx, sat in satellites_data.iterrows():
            debris_risk = self.classify_debris_risk(sat)
            if "HIGH" in debris_risk:
                alerts.append({
                    'type': 'DEBRIS',
                    'severity': 'HIGH',
                    'message': f"{sat.get('satellite_name', 'Unknown')}: {debris_risk}",
                    'risk_score': 70,
                    'timestamp': datetime.now()
                })
        
        # Sort by risk score
        alerts.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return alerts[:10]  # Return top 10 alerts
    
    def calculate_mission_impact(self, alerts: List[Dict], satellites_data: pd.DataFrame) -> Dict:
        """
        Calculate overall mission impact assessment
        """
        total_satellites = len(satellites_data)
        high_risk_count = len([a for a in alerts if a.get('severity') in ['HIGH', 'CRITICAL']])
        medium_risk_count = len([a for a in alerts if a.get('severity') == 'MEDIUM'])
        
        # Calculate overall risk level
        avg_risk_score = np.mean([a['risk_score'] for a in alerts]) if alerts else 0
        
        if avg_risk_score >= 75 or high_risk_count > 3:
            overall_status = "CRITICAL"
            recommendation = "Immediate action required. Review all high-risk conjunctions."
        elif avg_risk_score >= 50 or high_risk_count > 0:
            overall_status = "ELEVATED"
            recommendation = "Monitor closely. Prepare contingency plans."
        elif avg_risk_score >= 25:
            overall_status = "MODERATE"
            recommendation = "Routine monitoring. No immediate action required."
        else:
            overall_status = "NORMAL"
            recommendation = "All systems nominal. Continue standard operations."
        
        return {
            'overall_status': overall_status,
            'total_satellites': total_satellites,
            'high_risk_count': high_risk_count,
            'medium_risk_count': medium_risk_count,
            'average_risk_score': round(avg_risk_score, 2),
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }

if __name__ == "__main__":
    # Test risk assessment
    risk = RiskAssessment()
    
    test_risk = risk.calculate_collision_risk(3.5, 0.5, 0.05, 0.08)
    print(f"✅ Risk Assessment Test:")
    print(f"Risk Score: {test_risk['risk_score']}")
    print(f"Threat Level: {test_risk['threat_level']}")
