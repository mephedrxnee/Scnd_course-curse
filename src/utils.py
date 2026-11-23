from src.airplane import Airplane


def filter_airplanes(airplanes: list[Airplane], country: str) -> list[Airplane]:
    if not country:
        return airplanes
    return [a for a in airplanes if country.lower() in a.origin_country.lower()]


def get_airplanes_by_altitude(
    airplanes: list[Airplane], min_alt: float, max_alt: float
) -> list[Airplane]:
    return [a for a in airplanes if min_alt <= a.altitude <= max_alt]


def sort_airplanes(airplanes: list[Airplane], reverse: bool = True) -> list[Airplane]:
    return sorted(airplanes, key=lambda a: a.velocity, reverse=reverse)


def get_top_airplanes(airplanes: list[Airplane], top_n: int) -> list[Airplane]:
    return airplanes[:top_n]