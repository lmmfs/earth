import requests
from DB import queries, get_db

from logger import get_logger 

logger = get_logger(__name__)

def fetch_earthquake_data():
    response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson")

    if response.status_code >= 300:
        logger.warning(f"USGS invalid response code: {response.status_code}")
        return

    usgs_data = response.json().get('features', [])
    new_records_count = 0
    
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

            if id not in existing_ids:
                queries.add_new_record(db, earthquake_data)
                new_records_count += 1

    logger.info(f"Added new {new_records_count} records to database")
