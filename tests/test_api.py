from datetime import datetime
from zoneinfo import ZoneInfo
from http import HTTPStatus
from fastapi.testclient import TestClient
from .context import api
import pytest

client = TestClient(api.main.app)

MOCK_TIME_UTC = datetime(2025, 10, 15, 12, 30, 0, tzinfo=ZoneInfo("UTC"))

MOCK_EARTHQUAKES = (
    [
        {"id": "A1", "magnitude": 5.0, "time": MOCK_TIME_UTC, "latitude": 123.2, "longitude": 123.2, "depth" : 2.0},
        {"id": "B2", "magnitude": 6.2, "time": MOCK_TIME_UTC, "latitude": 123.2, "longitude": 123.2, "depth" : 2.0},
    ], 
    True
    )

MOCK_EARTHQUAKE = (
    {"id": "A1", "magnitude": 5.0, "time": MOCK_TIME_UTC, "latitude": 123.2, "longitude": 123.2, "depth" : 2.0},
    True
    )

def test_get_earthquakes_success(mocker):
    mocker.patch(
        "api.main.retrieve_recent_earthquakes", 
        return_value=MOCK_EARTHQUAKES
    )
    
    response = client.get("/earthquakes?limit=2")
    
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2
    assert response.json()[0]["magnitude"] == 5.0


def test_get_earthquakes_not_found(mocker):
    mocker.patch(
        "api.main.retrieve_recent_earthquakes", 
        return_value=(None, False)
    )

    response = client.get("/earthquakes")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_earthquakes_invalid_magnitute_interval():
    response = client.get("/earthquakes?min_magnitude=10&max_magnitude=2")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_earthquakes_invalid_date_interval():
    response = client.get("/earthquakes?after=2025-01-01T00:00:00Z&before=2024-01-01T00:00:00Z")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_earthquakes_by_id_success(mocker):
    mocker.patch(
        "api.main.retrieve_specific_earthquake", 
        return_value=MOCK_EARTHQUAKE
    )
    
    response = client.get("/earthquakes/A1")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == MOCK_EARTHQUAKE[0]["id"]
    assert response.json()["magnitude"] == MOCK_EARTHQUAKE[0]["magnitude"]


def test_get_earthquakes_by_id_not_found(mocker):
    mocker.patch(
        "api.main.retrieve_specific_earthquake", 
        return_value=(None, False)
    )
    
    response = client.get("/earthquakes/A2")
    
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("invalid_path", [
    "/earthquakes/ ",
    "/earthquakes/I D"
])
def test_get_earthquakes_by_id_missing_id(invalid_path):
    print(invalid_path)
    response = client.get(invalid_path)
    assert response.status_code == HTTPStatus.NOT_FOUND