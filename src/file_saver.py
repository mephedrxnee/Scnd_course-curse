import json
import os
from abc import ABC, abstractmethod
from src.airplane import Airplane


class BaseFileSaver(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_airplane(self, airplane: Airplane) -> None:
        pass

    @abstractmethod
    def get_airplanes(self, criteria: dict = None) -> list[Airplane]:
        pass

    @abstractmethod
    def delete_airplane(self, callsign: str) -> bool:
        pass


class JSONSaver(BaseFileSaver):
    """Класс для сохранения самолетов в JSON-файл."""

    def __init__(self, filename: str = "data/airplanes.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_file(self) -> list[dict]:
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data: list[dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_airplane(self, airplane: Airplane) -> None:
        data = self._read_file()
        for item in data:
            if item["callsign"] == airplane.callsign:
                return
        data.append({
            "callsign": airplane.callsign,
            "origin_country": airplane.origin_country,
            "velocity": airplane.velocity,
            "altitude": airplane.altitude,
        })
        self._write_file(data)

    def get_airplanes(self, criteria: dict = None) -> list[Airplane]:
        data = self._read_file()
        airplanes = [
            Airplane(
                item["callsign"], item["origin_country"],
                item["velocity"], item["altitude"]
            ) for item in data
        ]
        if criteria:
            result = []
            for a in airplanes:
                match = True
                if "origin_country" in criteria and criteria["origin_country"].lower() not in a.origin_country.lower():
                    match = False
                if "min_altitude" in criteria and a.altitude < criteria["min_altitude"]:
                    match = False
                if "max_altitude" in criteria and a.altitude > criteria["max_altitude"]:
                    match = False
                if match:
                    result.append(a)
            return result
        return airplanes

    def delete_airplane(self, callsign: str) -> bool:
        data = self._read_file()
        new_data = [item for item in data if item["callsign"] != callsign]
        if len(data) != len(new_data):
            self._write_file(new_data)
            return True
        return False