from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.testclient import TestClient
from .context import api

client = TestClient(api.main.app)

MOCK_TIME_UTC = datetime(2025, 10, 15, 12, 30, 0, tzinfo=ZoneInfo("UTC"))

MOCK_EARTHQUAKES = (
    [
        {"id": "A1", "magnitude": 5.0, "time": MOCK_TIME_UTC, "latitude": 123.2, "longitude": 123.2, "depth" : 2.0},
        {"id": "B2", "magnitude": 6.2, "time": MOCK_TIME_UTC, "latitude": 123.2, "longitude": 123.2, "depth" : 2.0},
    ], 
    True
    )

def test_get_earthquakes_success(mocker):
    mocker.patch(
        "api.main.retrieve_recent_earthquakes", 
        return_value=MOCK_EARTHQUAKES
    )
    
    response = client.get("/earthquakes?limit=2")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["magnitude"] == 5.0

def test_get_earthquakes_not_found(mocker):
    mocker.patch(
        "api.main.retrieve_recent_earthquakes", 
        return_value=(None, False)
    )

    response = client.get("/earthquakes")
    assert response.status_code == 404

