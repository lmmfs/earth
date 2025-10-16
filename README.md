
# Earthquake Python Rest API

A Rest API developed in python using fast api to collect data from USGS services




## Deployment

To deploy this project

clone the github repository
```bash
  git clone https://github.com/lmmfs/earth.git
```
start the services

```bash
  docker compose up
```


## API Reference

#### Get most recent earthquake records

```http
  GET /earthquakes
```

| Parameter | Type | Default | Description |
| :-------- | :--- | :------ | :---------- |
| `offset` | `int` | `0` | The number of records to skip (for pagination). |
| `limit` | `int` | `10` | The maximum number of records to return per page. |
| `min_magnitude` | `float` | `0.0` | Minimum magnitude (inclusive, e.g., magnitude >= min_magnitude). |
| `max_magnitude` | `float` | `20.0` | Maximum magnitude (inclusive, e.g., magnitude <= max_magnitud). |
| `after` | `datetime` | (None) | Filter for records occurring on or after this date/time (ISO 8601 format). |
| `before` | `datetime` | (None) | Filter for records occurring on or before this date/time (ISO 8601 format). |

|HTTP Status Code	| Description           |
| :---------------- | :-------------------- |
|200 OK	            | Successfully returned the most recent earthquake records.|
|404 Not Found	    | No earthquake record exists with the provided ID.|


#### Get earthquake record

```http
  GET /earthquakes/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of record to fetch |

|HTTP Status Code	| Description           |
| :---------------- | :-------------------- |
|200 OK	            | Successfully returned the specific earthquake record.|
|404 Not Found	    | No earthquake record exists with the provided ID.|


## Brief notes on design decisions

### Database schema
For the database schema I add these colums

- id - VARCHAR(50) primary_key
- magnitude - FLOAT
- time - DATETIME
- location - VARCHAR(255)
- latitude - FLOAT
- longitude - FLOAT
- depth - FLOAT

I decided to use the UGSS id as the primary key for my DB, since in the records it was already a unique value, so I don't to create my own unique ids.  
The limitation might be since if is necessary to add a source of earthquake data it is needed to change how the ids are stored maybe a combination of source + the unique of the record within that source  


### Project structure
```text
.
├── api
│   ├── data_loader.py
│   ├── data_requester.py
│   ├── DB
│   │   ├── db.py
│   │   ├── decoders.py
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── queries.py
│   │   └── schemas.py
│   ├── Dockerfile
│   ├── logger.py
│   ├── main.py
│   └── requirements.txt
├── data
├── docker-compose.yaml
└── README.md
```

The root of the project is  docker-compose.yaml to start the db service and api service. The api folder will be for the api code and data folder will be a volume for the db container  
In api folder I decided to create DB module to store all methods that interact with the database. I though it made the code more organized.  
On thing that I decided was to have the metdhods tha call the db queries on data_loader.py and data_requester.py, making that on main.py you only have the API routes. The though bewind this was to make the main only be responsable with the results and http responses. 

### Database configuration values

### Project notes
#### database creation
I decided to make the api create the database on api startup, like this
```code
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine) 
```
I decided on this given the scope of this project on having only one table on the database, the objective was to make easy as possible to setup, without touching directlly on the database container.   
The problem with this approach is if there are changes to model, like adding a new column to the table. The `create_all()` method will not pick up on the changes and we will need a database migration tool.

#### get_db
During the developement, it was needed to add `asynccontextmanager` because of fastapi lifespan, with that I learn about python context manager and found that it might be useful to use something similar when dealing with database requests.  
So I added the method `get_db()` on the DB model
```code
@contextmanager
def get_db():
    """Provides a transactional scope for db operations"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```
With this I can do basic error handling when quering the database, and given that use `with get_db() as db:`, it will close the connenction in the of the code block.  
The code was done focused on having only one table on the databse, but this behaviour can be imporved to deal with different tables on the database

## Roadmap

- compose set api url

- Add unit-tests

- fix container creates folders as root

