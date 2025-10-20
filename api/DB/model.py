from sqlalchemy import Column, DateTime, String, Float

from .db import Base
from .decoders import UnixTimestampMs 

class Earthquake(Base):
    __tablename__ = "earthquakes"

    # Use the id from USGS
    id = Column(String(50), primary_key=True)
    magnitude = Column(Float)
    # Parser to datetime from unix timestamp
    time = Column(UnixTimestampMs)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    depth = Column(Float)