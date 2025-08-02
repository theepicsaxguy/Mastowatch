from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.state_enum import StateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ShallowQuote")


@_attrs_define
class ShallowQuote:
    """Represents a quote or a quote placeholder, with the current authorization status.

    Example:
        {'state': 'accepted', 'quoted_status_id': '103270115826048975'}

    Attributes:
        state (StateEnum):
        quoted_status_id (Union[None, Unset, str]): The identifier of the status being quoted, if the quote has been
            accepted. This will be `null`, unless the `state` attribute is `accepted`.
    """

    state: StateEnum
    quoted_status_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        quoted_status_id: Union[None, Unset, str]
        if isinstance(self.quoted_status_id, Unset):
            quoted_status_id = UNSET
        else:
            quoted_status_id = self.quoted_status_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
            }
        )
        if quoted_status_id is not UNSET:
            field_dict["quoted_status_id"] = quoted_status_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        state = StateEnum(d.pop("state"))

        def _parse_quoted_status_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        quoted_status_id = _parse_quoted_status_id(d.pop("quoted_status_id", UNSET))

        shallow_quote = cls(
            state=state,
            quoted_status_id=quoted_status_id,
        )

        shallow_quote.additional_properties = d
        return shallow_quote

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
