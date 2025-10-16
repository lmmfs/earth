from datetime import datetime
from typing import List, Optional
from DB import queries, EarthquakeResponse, get_db, Earthquake
from constants import MAX_MAGNITUDE, MIN_MAGNITUDE
from logger import get_logger

logger = get_logger(__name__) 

def retrieve_recent_earthquakes(
        offset: int, 
        limit: int, 
        min_magnitude: float, 
        max_magnitude: float,
        after: Optional[datetime], 
        before: Optional[datetime]
        ) -> tuple[List[EarthquakeResponse] | None, bool]:
    logger.info(f"Requisting {limit} records, index = {offset}")
    stmt = queries.get_base_select_statement()

    if min_magnitude > MIN_MAGNITUDE:
        logger.info(f"setting min magnitude from {min_magnitude}")
        stmt = stmt.where(Earthquake.magnitude >= min_magnitude)
    
    if max_magnitude < MAX_MAGNITUDE:
        logger.info(f"setting max magnitude to {max_magnitude}")
        stmt = stmt.where(Earthquake.magnitude <= max_magnitude)

    if before:
        stmt = stmt.where(Earthquake.time <= before)

    if after:
        stmt = stmt.where(Earthquake.time >= after)

    stmt = stmt.order_by(Earthquake.time.desc()).offset(offset).limit(limit)
    
    with get_db() as db:
        results =  queries.execute_select(db, stmt)
        if results:
            return results, True
        
        return None, False
    

def retrieve_specific_earthquake(earthquake_id: str) -> tuple[EarthquakeResponse | None, bool]:
    with get_db() as db:
        result = queries.select_earthquake_with_id(db, earthquake_id)
        if result:
            return result[0], True
        
        return None, False
            