import requests
from db import SessionLocal
from model import Earthquake

def fetch_earthquake_data():
    response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")
    data = response.json()

    db = SessionLocal()
    for feature in data["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        eq = Earthquake(
            magnitude=props["mag"],
            place=props["place"],
            time=props["time"],
            latitude=coords[1],
            longitude=coords[0]
        )
        db.add(eq)
    db.commit()
    db.close()