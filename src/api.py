from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class NominatimAPI(BaseAPI):
    """Класс для получения координат страны."""

    def get_data(self, country: str) -> list[float] | None:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": country, "format": "json"}
        headers = {"User-Agent": "CourseworkApp/1.0"}

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                return None

            bbox = data[0]["boundingbox"]
            return [float(coord) for coord in bbox]
        except requests.exceptions.RequestException:
            return None


class OpenSkyAPI(BaseAPI):
    """Класс для получения данных о самолетах."""

    def get_data(self, bbox: list[float]) -> list[dict]:
        if not bbox or len(bbox) != 4:
            return []

        url = "https://opensky-network.org/api/states/all"
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3],
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            states = data.get("states", [])
            if not states:
                return []

            airplanes = []
            for state in states:
                airplanes.append({
                    "callsign": state[1].strip() if state[1] else "Unknown",
                    "origin_country": state[2],
                    "velocity": state[9] if state[9] else 0.0,
                    "altitude": state[13] if state[13] else 0.0
                })
            return airplanes
        except requests.exceptions.RequestException:
            return []