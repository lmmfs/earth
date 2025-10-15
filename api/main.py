from contextlib import asynccontextmanager
from fastapi import FastAPI
from DB import engine, Base, model

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print('Hello')
    from data_loader import fetch_earthquake_data
    fetch_earthquake_data()
    yield
    # Shutdown
    

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Earthquake API is running!"}