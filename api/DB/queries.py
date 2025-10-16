from typing import List, Tuple
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from logger import get_logger
from .db import engine
from .model import Earthquake
from .schemas import EarthquakeResponse

logger = get_logger(__name__) 

def select_ids(db: Session) -> set[str]:
    """
    Select the ids of records on table

    Select all the ids of the earthquake records from earthquake table

    :param db: Session for the database connection.
    :type db: Session
    :returns: set with all the record ids.
    :rtype: set[str]
    """
    stmt = select(Earthquake.id)
    
    result = db.execute(stmt).scalars().all()

    return set(result)

def insert_new_record(db: Session, record_data: dict):
    """
    Insert a new record on table

    Insert into earthquake table a new a record, with data from a dictionary
    
    :param db: Session for the database connection.
    :type db: Session
    :param record_data: Dictionary with the record data.
    :type record_data: dict
    """
    new_record = Earthquake(**record_data)
    
    db.add(new_record)


def get_base_select_statement():
    """
    Get a basic select statement to the earthquake table
    
    SELECT * FROM earthquakes 

    :returns: Select statement.
    :rtype: Select[Tuple[Earthquake]]
    """
    return select(Earthquake)


def execute_select(db: Session, statement:Select[Tuple[Earthquake]])-> List[EarthquakeResponse]:
    """
    Executes a select statement on the earthquake table

    :param db: Session for the database connection.
    :type db: Session
    :param statement: The select statement.
    :type statement: Select[Tuple[Earthquake]]
    :returns: The result of the select.
    :rtype: List[EarthquakeResponse]
    """
    results = db.execute(statement).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]

    logger.info(f"Successfully retrieved {len(response_list)} records.")
    
    return response_list


def select_earthquake_with_id(db: Session, id: str) -> List[EarthquakeResponse]:
    """
    Select specific earthquake record

    Select earthquake record from the earthquake table,
    given a specific id

    :param db: Session for the database connection.
    :type db: Session
    :param id: The id os the earthquake record.
    :type id: str
    :returns: The result of the select.
    :rtype: List[EarthquakeResponse]
    """
    logger.info(f"Attempt to retrieve record with id {id}")

    stmt = select(Earthquake).where(Earthquake.id == id)

    results = db.execute(stmt).scalars().all()

    response_list = [
        EarthquakeResponse.model_validate(record) 
        for record in results
    ]
    
    return response_list
