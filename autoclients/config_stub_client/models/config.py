from typing import Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Config")


@_attrs_define
class Config:
    """Сущность конфига.

    Attributes:
        id (UUID):
        min_cost (float):
        rubles_per_meter (float):
    """

    id: UUID
    min_cost: float
    rubles_per_meter: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = str(self.id)

        min_cost = self.min_cost

        rubles_per_meter = self.rubles_per_meter

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "min_cost": min_cost,
                "rubles_per_meter": rubles_per_meter,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = UUID(d.pop("id"))

        min_cost = d.pop("min_cost")

        rubles_per_meter = d.pop("rubles_per_meter")

        config = cls(
            id=id,
            min_cost=min_cost,
            rubles_per_meter=rubles_per_meter,
        )

        config.additional_properties = d
        return config

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
