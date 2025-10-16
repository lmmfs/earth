from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from DB import engine, Base, model
from constants import MAX_MAGNITUDE, MIN_MAGNITUDE
from data_requester import retrieve_recent_earthquakes, retrieve_specific_earthquake
from logger import get_logger

app = FastAPI()
app_logger = get_logger("API_MAIN") 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app_logger.info("Logger initialized")
    Base.metadata.create_all(bind=engine)
    # Request USGS data on app startup
    from data_loader import fetch_earthquake_data
    fetch_earthquake_data()
    yield
    # Shutdown
    

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Earthquake API is running!"}


@app.get("/earthquakes")
def get_recent_earthquakes(
    offset: int = 0, 
    limit: int = 10, 
    min_magnitude: float = MIN_MAGNITUDE,
    max_magnitude: float = MAX_MAGNITUDE,
    after: Optional[datetime] = None,
    before: Optional[datetime] = None,
    ):
    if max_magnitude < min_magnitude:
        raise HTTPException(status_code=404, detail="records not found")

    if after and before and before < after:
        raise HTTPException(status_code=404, detail="records not found")
    
    records, found = retrieve_recent_earthquakes(offset, limit, min_magnitude, max_magnitude, after, before)
    
    if not found:
        raise HTTPException(status_code=404, detail="records not found")

    return records


@app.get("/earthquakes/{earthquake_id}")
def get_specific_earthquake(earthquake_id: str):
    if not earthquake_id:
        app_logger.warning("empty id requested")
        raise HTTPException(status_code=404, detail="record not found")
    
    record, found = retrieve_specific_earthquake(earthquake_id)

    if not found:
        raise HTTPException(status_code=404, detail="record not found")

    return record