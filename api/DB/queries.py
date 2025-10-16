from typing import List, Tuple
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from logger import get_logger
from .db import engine
from .model import Earthquake
from .schemas import EarthquakeResponse

logger = get_logger(__name__) 

# Select from Earthquake table all ids
# returns as a set of strings
def get_all_existing_ids(db: Session) -> set[str]:
    stmt = select(Earthquake.id)
    
    result = db.execute(stmt).scalars().all()

    return set(result)

# Insert into Earthquake table a new earthquake id
def add_new_record(db: Session, record_data: dict):
    new_record = Earthquake(**record_data)
    
    db.add(new_record)


def get_base_select_statement():
    return select(Earthquake)


def execute_select(db: Session, statement:Select[Tuple[Earthquake]])-> List[EarthquakeResponse]:
    results = db.execute(statement).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]

    logger.info(f"Successfully retrieved {len(response_list)} records.")
    
    return response_list


# Select from Earthquake most recent n earthquakes
# limit: int
# returns as a set of strings
def select_last_n_recent_earthquakes(db: Session, limit: int) -> List[EarthquakeResponse]:
    query_limit = max(limit, 1)

    logger.info(f"Attempt to retrieve {query_limit} records.")
        
    stmt = select(Earthquake).order_by(Earthquake.time.desc()).limit(query_limit)

    results = db.execute(stmt).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]

    logger.info(f"Successfully retrieved {len(response_list)} records.")
    
    return response_list


def select_earthquake_with_id(db: Session, id: str) -> List[EarthquakeResponse]:
    logger.info(f"Attempt to retrieve record with id {id}")

    stmt = select(Earthquake).where(Earthquake.id == id)

    results = db.execute(stmt).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]
    
    return response_list
