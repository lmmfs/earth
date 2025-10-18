
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
  cd earth
  docker compose up
```

with the default configuration the  API will be available at http://0.0.0.0:8000  
to change this configuration is need to change the docker-compose.yaml 

## Local Development Setup

If you prefer to run the API locally (outside of Docker), use the setup script to install all Python dependencies in your environment.
### Install dependencies

Run the setup script to install locally the python dependencies the root of the project.  
It will install the dependencies for used in the api module and for tests

```bash
  cd earth
  python3 setup.py
```

## Running Tests

To run tests, run the pytest command on the root of the project

```bash
  cd earth
  pytest
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
| `max_magnitude` | `float` | `20.0` | Maximum magnitude (inclusive, e.g., magnitude <= max_magnitude). |
| `after` | `datetime` | (None) | Filter for records occurring on or after this date/time (ISO 8601 format). |
| `before` | `datetime` | (None) | Filter for records occurring on or before this date/time (ISO 8601 format). |

|HTTP Status Code	| Description           |
| :---------------- | :-------------------- |
|200 OK	            | Successfully returned the most recent earthquake records.|
|404 Not Found	    | No earthquake record exists with the provided ID.|
|400 Bad Request	  | If the magnitude interval is invalid i.e max_magnitude > min_magnitude.|
|400 Bad Request	  | If the date interval is invalid i.e before < after.|


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
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   └── Utils
│       ├── constants.py
│       ├── __init__.py
│       └── logger.py
├── data 
├── .devcontainer
│   ├── devcontainer.json
│   ├── docker-compose.dev.yml
│   └── Dockerfile.dev
├── docker-compose.yaml
├── Dockerfile
├── logs
|   ├── placeholder.txt
│   └── app.log
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── templatedata.json
└── tests
    ├── context.py
    ├── __init__.py
    └── test_api.py
```

The root of the project is docker-compose.yaml to start the db service and api service. The api folder will be for the api code and data folder will be a volume for the db container.  
On the api module the design was focused on separated concerns: main.py handles API routing and HTTP responses; data_loader.py and data_requester.py handle data flow; and the dedicated DB module encapsulates all database interaction logic.  
My main was simple organization of the code

### Dev container
For development, the project relies on the VS Code Dev Containers extension and the files defined in the .devcontainer folder. This setup ensures a consistent, isolated development environment that mirrors the final environment, providing both the database and the API code running inside containers.

### Database schema
For the database schema I add these columns

- id - VARCHAR(50) primary_key
- magnitude - FLOAT
- time - DATETIME
- location - VARCHAR(255)
- latitude - FLOAT
- longitude - FLOAT
- depth - FLOAT

I decided to use the USGS id as the primary key for my DB, since in the records it was already a unique value, so I didn't create my own unique ids. 
This approach will require changing the ID structure (making a composite key combining source + unique_record_id) if its necessary to add data from multiple earthquake sources.

### API design
When design the API, my assumption was that the service would request data to USGS and stored in the database, then on each request is mapped to a select statement on the database.  
For the earthquakes/ get endpoint, I assumed that the most recent records is referring to the earth record timestamp so the select is ordered by this datetime.  
This creates a limitation when I added a scheduler to call the method that collects data every 10 seconds. The earthquakes/ get endpoint became not idempotent because the values for the most recent earthquakes might change. The query parameters for filtering (specially the date intervals) might reduce the variance of the results

### Query filtering

One of the extra objectives was to add filtering to the get endpoint based on magnitude and time.  
To implement tis filtering I had 2 ideas. 

- Add a value, and a variable for the condition (e.g. earthquakes?magnitude=5.0&value=greater)

- Add bound limits to the maximum and minimum that value can have (e.g. earthquakes?max_magnitude=5.0&min_magnitude=1.0)

I decided on going with the second option, is simpler for a user to set the values that he wants, is simpler on implementation since is not need to check the different values for the relation like greater or lesser. This way is also simpler to map to the select query.  
Also add a basic condition to validate if the interval is valid (e.g. max > min), and return BAD REQUEST is the condition is not satisfied.

### logs placeholder
during the development, an issue that I encountered was the creation of the log folder, when I added the log folder as a docker compose volume, if this folder didn't exist it was created by the user root, this resulted on permission errors when running the app.  
To solve this I decided on locally create the log folder, and put a placeholder file in it so it would be keep on the git repo. 

### Database creation
I decided to make the api create the database on api startup, like this
```code
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine) 
```
I decided on this given the scope of this project on having only one table on the database, the objective was to make easy as possible to setup, without touching directly on the database container.   
The limitation is that approach does not support schema evolution. Any future model changes (e.g., adding a new column) are not caught by `create_all()` method. It would require integrating a database migration tool (like Alembic).

### Database configuration values
Giving the size of the project scope, the configuration for the database is defined on the docker-compose.yaml.  
In the future some of these value should be moved to a Docker secret for better security.

### get_db function
During the development, it was needed to add `asynccontextmanager` because of fastapi lifespan, with that I learn about python context manager and found that it might be useful to use something similar when dealing with database requests.  
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
With this I can do basic error handling when querying the database, and given that use `with get_db() as db:`, it will close the connection in the of the code block.  
The code was done focused on having only one table on the database, but this behavior can be improved to deal with different tables on the database

