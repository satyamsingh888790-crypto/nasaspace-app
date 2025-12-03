import csv
import random
from datetime import datetime, timedelta
import os

data_folder = "."
NUM_SATS = 20
NUM_OBSERVERS = 5
sample_images = [
    "https://images-assets.nasa.gov/image/PIA14417/PIA14417~medium.jpg",
    "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001465/GSFC_20171208_Archive_e001465~small.jpg",
    "https://images-assets.nasa.gov/image/PIA04216/PIA04216~small.jpg",
    "https://images-assets.nasa.gov/image/PIA04220/PIA04220~small.jpg",
    "https://images-assets.nasa.gov/image/PIA04225/PIA04225~medium.jpg"
]

def generate_mock_tle(norad_id):
    line1 = f"1 {norad_id:05d}U 20001A   25276.{random.randint(10000000,99999999)}  .0000{random.randint(100,999)}  00000+0  12345-3 0  999{random.randint(0,9)}"
    line2 = f"2 {norad_id:05d}  {random.randint(0,90):05.4f}  {random.randint(0,360):05.4f} {random.randint(0,999999):06d} {random.randint(0,360):06.3f}  {random.randint(0,360):06.3f} {random.uniform(0,20):0.8f} {random.randint(10000,99999)}"
    return line1, line2

# 1️⃣ Mock TLE
with open(os.path.join(data_folder, "mock_tle.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["satellite_name", "norad_id", "line1", "line2", "timestamp"])
    for i in range(NUM_SATS):
        norad_id = 900+i
        line1, line2 = generate_mock_tle(norad_id)
        timestamp = datetime.utcnow() + timedelta(minutes=random.randint(-60,60))
        writer.writerow([f"SAT-{norad_id}", norad_id, line1, line2, timestamp.isoformat()+"Z"])

# 2️⃣ Mock Radar
with open(os.path.join(data_folder, "mock_radar.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["satellite_name", "norad_id", "radar_range_km", "radar_velocity_km_s", "radar_cross_section_m2", "timestamp"])
    for i in range(NUM_SATS):
        norad_id = 900+i
        timestamp = datetime.utcnow() + timedelta(minutes=random.randint(-60,60))
        writer.writerow([f"SAT-{norad_id}", norad_id, round(random.uniform(400,1200),2), round(random.uniform(7,8),2), round(random.uniform(0.01,0.1),3), timestamp.isoformat()+"Z"])

# 3️⃣ Mock Optical
with open(os.path.join(data_folder, "mock_optical.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["satellite_name", "norad_id", "optical_image_url", "timestamp", "observer_lat", "observer_lon", "observer_alt"])
    for i in range(NUM_SATS):
        norad_id = 900+i
        timestamp = datetime.utcnow() + timedelta(minutes=random.randint(-60,60))
        writer.writerow([f"SAT-{norad_id}", norad_id, random.choice(sample_images), timestamp.isoformat()+"Z", round(random.uniform(-90,90),4), round(random.uniform(-180,180),4), round(random.uniform(0,5),2)])

# 4️⃣ Mock Space Weather
with open(os.path.join(data_folder, "mock_space_weather.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "solar_flare_class", "kp_index", "solar_wind_speed_km_s", "atmospheric_density"])
    for i in range(50):
        timestamp = datetime.utcnow() + timedelta(minutes=i*10)
        writer.writerow([timestamp.isoformat()+"Z", random.choice(["A","B","C","M","X"]), random.randint(0,9), round(random.uniform(300,800),1), round(random.uniform(1e-12,1e-10),12)])

# 5️⃣ Mock Observers
with open(os.path.join(data_folder, "mock_observer.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["observer_name","lat","lon","alt_m","timestamp","field_of_view_deg"])
    for i in range(NUM_OBSERVERS):
        timestamp = datetime.utcnow()
        writer.writerow([f"OBS-{i+1}", round(random.uniform(-90,90),4), round(random.uniform(-180,180),4), round(random.uniform(0,5),2), timestamp.isoformat()+"Z", round(random.uniform(30,120),1)])

# 6️⃣ Mock Lightcurve
with open(os.path.join(data_folder, "mock_lightcurve.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["satellite_name", "norad_id", "timestamp", "brightness", "rotation_rate_deg_s"])
    for i in range(NUM_SATS):
        norad_id = 900+i
        for j in range(5):  # 5 time points
            timestamp = datetime.utcnow() + timedelta(minutes=j*10)
            writer.writerow([f"SAT-{norad_id}", norad_id, timestamp.isoformat()+"Z", round(random.uniform(0,200),1), round(random.uniform(0.1,5),2)])

# 7️⃣ Mock Spectral
with open(os.path.join(data_folder, "mock_spectral.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["satellite_name", "norad_id", "timestamp", "spectral_uv", "spectral_visible", "spectral_ir"])
    for i in range(NUM_SATS):
        norad_id = 900+i
        timestamp = datetime.utcnow()
        writer.writerow([f"SAT-{norad_id}", norad_id, timestamp.isoformat()+"Z", round(random.uniform(0,1),2), round(random.uniform(0,1),2), round(random.uniform(0,1),2)])

print("✅ All mock CSV files generated in the current folder!")