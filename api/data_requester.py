from typing import List
from DB import queries, EarthquakeResponse, get_db

def retrieve_recent_earthquakes() -> List[EarthquakeResponse]:
    with get_db() as db:
        return queries.select_last_n_recent_earthquakes(db, 10)
    

def retrieve_specific_earthquake(earthquake_id: str) -> tuple[EarthquakeResponse | None, bool]:
    with get_db() as db:
        result = queries.select_earthquake_with_id(db, earthquake_id)
        if result:
            return result[0], True
        
        return None, False
            