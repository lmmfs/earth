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
    """
    Retrieve from database the most recent earthquake records
    
    This method retrieves data from the earthquake table according,
    to query parameters
    
    :param offset: The number of records to skip (for pagination).
    :type offset: int
    :param limit: The maximum number of records to return.
    :type limit: int
    :param min_magnitude: The minimum value for earthquake magnitude.
    :type min_magnitude: float
    :param max_magnitude: The maximum value for earthquake magnitude.
    :type max_magnitude: float
    :param after: The datetime for records occurring on or after this date/time.
    :type after: Optional[datetime]
    :param after: The datetime for records occurring on or before this date/time.
    :type after: Optional[datetime]
    :returns: (List[EarthquakeResponse], True) if it found records on the table, (None, False) otherwise.
    :rtype: tuple[List[EarthquakeResponse] | None, bool]
    """

    logger.info(f"Requesting {limit} records, index = {offset}")
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
    """
    Retrieve from database for a specific earthquake record
    
    This method retrieves data from a specific earthquake table entry,
    given a specific record id
    
    :param earthquake_id: The specific id of the earthquake record.
    :type earthquake_id: str
    :returns: (EarthquakeResponse, True) if it found the record on the table, (None, False) otherwise.
    :rtype: tuple[EarthquakeResponse | None, bool]
    """
    with get_db() as db:
        result = queries.select_earthquake_with_id(db, earthquake_id)
        if result:
            return result[0], True
        
        return None, False
            