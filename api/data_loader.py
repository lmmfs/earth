import requests
from DB import queries
from DB import Earthquake
from DB import get_db

def fetch_earthquake_data():
    response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")

    response.raise_for_status()
    usgs_data = response.json().get('features', [])

    
    with get_db() as db:

        existing_ids = queries.get_all_existing_ids(db)

        print(existing_ids)

        for feature in usgs_data:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            id = feature["id"]

            earthquake_data = {
                "id" : id,
                "magnitude" : props["mag"],
                "location" : props["place"],
                "time" : props["time"],
                "latitude" : coords[1],
                "longitude" : coords[0],
                "depth" : coords[2]
            }

            #queries.add_new_record(db, earthquake_data)
            break
