from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import engine
from .model import Earthquake
from .schemas import EarthquakeResponse

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


# Select from Earthquake most recent n earthquakes
# limit: int
# returns as a set of strings
def select_last_n_recent_earthquakes(db: Session, limit: int) -> List[EarthquakeResponse]:
    query_limit = max(limit, 1)
        
    stmt = select(Earthquake).order_by(Earthquake.time.desc()).limit(query_limit)

    results = db.execute(stmt).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]
    
    return response_list


def select_earthquake_with_id(db: Session, id: str) -> List[EarthquakeResponse]:
    stmt = select(Earthquake).where(Earthquake.id == id)

    results = db.execute(stmt).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]
    
    return response_list
