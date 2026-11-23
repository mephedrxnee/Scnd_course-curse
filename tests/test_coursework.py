import pytest
from unittest.mock import Mock
from src.airplane import Airplane
from src.api import NominatimAPI, OpenSkyAPI
from src.file_saver import JSONSaver
from src.utils import filter_airplanes, sort_airplanes, get_top_airplanes


# Тесты для Airplane (Задание 2)
def test_airplane_validation():
    with pytest.raises(ValueError):
        Airplane("A1", "Country", -100, 1000)  # Отрицательная скорость


def test_airplane_comparison():
    plane1 = Airplane("A1", "Country", 200, 10000)
    plane2 = Airplane("A2", "Country", 300, 5000)
    assert plane1 < plane2
    assert plane2 > plane1


# Тесты для API (Задание 1)
def test_nominatim_api(mocker):
    mock_response = Mock()
    mock_response.json.return_value = [{"boundingbox": ["1.0", "2.0", "3.0", "4.0"]}]
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    api = NominatimAPI()
    bbox = api.get_data("TestCountry")
    assert bbox == [1.0, 2.0, 3.0, 4.0]


def test_opensky_api(mocker):
    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [
            [
                "123", "UAL1", "USA", None, None, None,
                None, None, None, 250.0, None, None, None,
                10000.0, None, None, None
            ]
        ]
    }
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    api = OpenSkyAPI()
    planes = api.get_data([1.0, 2.0, 3.0, 4.0])
    assert len(planes) == 1
    assert planes[0]["callsign"] == "UAL1"
    assert planes[0]["velocity"] == 250.0
    assert planes[0]["altitude"] == 10000.0

    api = OpenSkyAPI()
    planes = api.get_data([1.0, 2.0, 3.0, 4.0])
    assert len(planes) == 1
    assert planes[0]["callsign"] == "UAL1"


# Тесты для JSONSaver (Задание 3)
@pytest.fixture
def temp_json_file(tmp_path):
    return str(tmp_path / "test_planes.json")


def test_json_saver_add_get_delete(temp_json_file):
    saver = JSONSaver(temp_json_file)
    plane = Airplane("TEST1", "Russia", 200, 10000)

    # Добавление
    saver.add_airplane(plane)
    saved_planes = saver.get_airplanes()
    assert len(saved_planes) == 1
    assert saved_planes[0].callsign == "TEST1"

    # Удаление
    assert saver.delete_airplane("TEST1") is True
    assert len(saver.get_airplanes()) == 0


# Тесты для утилит
def test_filter_and_sort():
    p1 = Airplane("A1", "Russia", 100, 5000)
    p2 = Airplane("A2", "USA", 300, 10000)

    filtered = filter_airplanes([p1, p2], "Russia")
    assert len(filtered) == 1
    assert filtered[0].callsign == "A1"

    sorted_planes = sort_airplanes([p1, p2], reverse=True)
    assert sorted_planes[0].callsign == "A2"
    assert len(get_top_airplanes(sorted_planes, 1)) == 1
