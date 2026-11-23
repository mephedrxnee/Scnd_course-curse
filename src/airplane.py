class Airplane:
    """Класс для описания самолета."""

    def __init__(
        self, callsign: str, origin_country: str, velocity: float, altitude: float
    ) -> None:
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = self._validate_numeric(velocity, "Скорость")
        self.altitude = self._validate_numeric(altitude, "Высота")

    @staticmethod
    def _validate_numeric(value: float, field_name: str) -> float:
        """Валидация числовых значений (Задание 2)."""
        if value is None:
            return 0.0
        try:
            val = float(value)
            if val < 0:
                raise ValueError(f"{field_name} не может быть отрицательной")
            return val
        except (ValueError, TypeError):
            raise ValueError(f"Некорректное значение для {field_name}")

    def __str__(self) -> str:
        return (
            f"{self.callsign} ({self.origin_country}), "
            f"Скорость: {self.velocity} м/с, Высота: {self.altitude} м"
        )

    def __lt__(self, other: 'Airplane') -> bool:
        """Сравнение по скорости, затем по высоте."""
        if self.velocity == other.velocity:
            return self.altitude < other.altitude
        return self.velocity < other.velocity

    def __gt__(self, other: 'Airplane') -> bool:
        """Сравнение по скорости, затем по высоте."""
        if self.velocity == other.velocity:
            return self.altitude > other.altitude
        return self.velocity > other.velocity
