from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import engine
from .model import Earthquake

def get_all_existing_ids(db: Session) -> set[str]:
    stmt = select(Earthquake.id)
    
    result = db.execute(stmt).scalars().all()

    return set(result)

# 
def add_new_record(db: Session, record_data: dict):
    new_record = Earthquake(**record_data)
    
    db.add(new_record)
