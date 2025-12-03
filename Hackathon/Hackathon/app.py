import os
import requests
import datetime
import csv
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
NASA_API_KEY = os.getenv("NASA_API_KEY", "yizMReSiSuuAm3ZAnp5OITUkuKKgRmPtnkz9f12B")
SPACETRACK_USER = os.getenv("SPACETRACK_USER", "ayan.pande2004@gmail.com")
SPACETRACK_PASS = os.getenv("SPACETRACK_PASS", "Ayanromanpande.202")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

# === NASA APOD (Astronomy Picture of the Day) ===
def fetch_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    r = requests.get(url)
    data = r.json()
    apod_path = os.path.join(DATA_DIR, f"nasa_apod_{today}.csv")
    with open(apod_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Title", "Explanation", "Image_URL"])
        writer.writerow([data["date"], data["title"], data["explanation"], data["url"]])
    print(f"✅ Saved APOD to {apod_path}")

# === NASA Image Library (Optical Telescope) ===
def fetch_nasa_images():
    url = "https://images-api.nasa.gov/search?q=telescope&media_type=image"
    r = requests.get(url)
    data = r.json()
    items = data["collection"]["items"][:10]
    image_links = [i["links"][0]["href"] for i in items]
    img_path = os.path.join(DATA_DIR, f"nasa_images_{today}.csv")
    with open(img_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Image_URL"])
        for link in image_links:
            writer.writerow([link])
    print(f"✅ Saved NASA images to {img_path}")

# === NASA Space Weather Data ===
def fetch_space_weather():
    url = f"https://api.nasa.gov/DONKI/FLR?startDate={today}&endDate={today}&api_key={NASA_API_KEY}"
    r = requests.get(url)
    data = r.json()
    sw_path = os.path.join(DATA_DIR, f"nasa_space_weather_{today}.csv")
    with open(sw_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Flare_ID", "PeakTime", "ClassType"])
        if len(data) == 0:
            writer.writerow(["No recent flares", "", ""])
        else:
            for flare in data:
                writer.writerow([flare["flrID"], flare["peakTime"], flare["classType"]])
    print(f"✅ Saved space weather data to {sw_path}")

# === SPACE-TRACK TLE ===
def fetch_tle():
    session = requests.Session()
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/format/tle"

    login_data = {"identity": SPACETRACK_USER, "password": SPACETRACK_PASS}
    session.post(login_url, data=login_data)

    r = session.get(query_url)
    tle_data = r.text.strip()

    tle_path_txt = os.path.join(DATA_DIR, f"space_track_tle_{today}.txt")
    with open(tle_path_txt, "w", encoding="utf-8") as f:
        f.write(tle_data)

    # Also save as CSV
    tle_path_csv = os.path.join(DATA_DIR, f"space_track_tle_{today}.csv")
    with open(tle_path_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Line"])
        for line in tle_data.splitlines():
            writer.writerow([line])

    print(f"✅ Saved TLE data to {tle_path_txt} and {tle_path_csv}")

# === MAIN ===
if __name__ == "__main__":
    print("Fetching NASA and Space-Track data...")
    fetch_apod()
    fetch_nasa_images()
    fetch_space_weather()
    fetch_tle()
    print("🎉 All data successfully fetched and saved in /data folder.")