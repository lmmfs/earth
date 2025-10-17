from contextlib import contextmanager
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.Utils.logger import get_logger

DATABASE_URL = "postgresql://user:password@db:5432/earthquakes"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

logger = get_logger(__name__)

@contextmanager
def get_db():
    """
    Provides a transactional scope for db operations
    
    After scope db connection is closed on finally statement
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        logger.error("Database transaction failed. Performing rollback.", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()