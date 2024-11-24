from dataclasses import dataclass
from random import uniform
from typing import ClassVar, Self
from uuid import uuid4

from src.domain.entities.config import Config
from src.domain.services.interfaces.config import ConfigInterface


@dataclass
class ConfigAdapter(ConfigInterface):
    """Адаптер конфигурации."""

    _min_base_price: ClassVar[float] = 0.0
    _max_base_price: ClassVar[float] = 100.0

    _min_rubles_per_meter: ClassVar[float] = 0.05
    _max_rubles_per_meter: ClassVar[float] = 0.1

    _precision: ClassVar[int] = 2

    async def get(self: Self) -> "Config":
        """Получить конфигурацию."""
        min_cost = uniform(self._min_base_price, self._max_base_price)
        rubles_per_meter = uniform(self._min_rubles_per_meter, self._max_rubles_per_meter)

        return Config(
            id=uuid4(),
            min_cost=round(min_cost, self._precision),
            rubles_per_meter=round(rubles_per_meter, self._precision),
        )
