from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from api.DB import engine, Base, model
from api.Utils.constants import MAX_MAGNITUDE, MIN_MAGNITUDE, REFRESH_DATASET_INTERVAL_SECONDS
from api.Utils.logger import get_logger, setup_logging
from .data_loader import fetch_earthquake_data_opt
from .data_requester import retrieve_recent_earthquakes, retrieve_specific_earthquake

app = FastAPI()
setup_logging()
app_logger = get_logger("API_MAIN") 
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app_logger.info("Logger initialized")
    # Create database
    Base.metadata.create_all(bind=engine)
    # Request USGS data on 10 second interval
    scheduler.add_job(
        func=fetch_earthquake_data_opt, 
        trigger='interval', 
        seconds=REFRESH_DATASET_INTERVAL_SECONDS, 
        id='earthquake_fetcher',
        replace_existing=True
    )
    scheduler.start()
    yield
    # Shutdown
    app_logger.info("App shutting down")
    scheduler.shutdown()
    

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
    # Early check for query parameters
    if max_magnitude < min_magnitude:
        raise HTTPException(status_code=400, detail="invalid magnitudes")

    if after and before and before < after:
        raise HTTPException(status_code=400, detail="invalid date interval")
    
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