from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EarthquakeResponse(BaseModel):
    id: str
    magnitude: float
    time: datetime
    location: str
    latitude: float
    longitude: float
    depth: float
    
    model_config = ConfigDict(from_attributes=True)