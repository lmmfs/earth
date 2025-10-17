from datetime import datetime, timezone
from sqlalchemy.types import TypeDecorator, DateTime
from typing import Optional

class UnixTimestampMs(TypeDecorator):
    """
    Stores data as TIMESTAMP WITH TIME ZONE in the DB (impl=DateTime),
    converts millisecond Unix timestamps from Python to datetime objects.
    """
    impl = DateTime(timezone=True) 
    cache_ok = True

    def process_bind_param(self, value: Optional[int], dialect) -> Optional[datetime]:
        if value is None:
            return None
        
        # bypass if it is a datetime
        if isinstance(value, datetime):
            return value
        
        # Convert ms to seconds (float)
        timestamp_sec = value / 1000.0
        # Create a UTC datetime object from the timestamp
        return datetime.fromtimestamp(timestamp_sec, tz=timezone.utc)
        

    def process_result_value(self, value: Optional[datetime], dialect) -> Optional[datetime]:
        return value