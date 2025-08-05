from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.state_enum import StateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.status import Status


T = TypeVar("T", bound="Quote")


@_attrs_define
class Quote:
    """Represents a quote or a quote placeholder, with the current authorization status.

    Attributes:
        state (StateEnum):
        quoted_status (Union['Status', None, Unset]): The status being quoted, if the quote has been accepted. This will
            be `null`, unless the `state` attribute is `accepted`.
    """

    state: StateEnum
    quoted_status: Union["Status", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.status import Status

        state = self.state.value

        quoted_status: Union[None, Unset, dict[str, Any]]
        if isinstance(self.quoted_status, Unset):
            quoted_status = UNSET
        elif isinstance(self.quoted_status, Status):
            quoted_status = self.quoted_status.to_dict()
        else:
            quoted_status = self.quoted_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
            }
        )
        if quoted_status is not UNSET:
            field_dict["quoted_status"] = quoted_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.status import Status

        d = dict(src_dict)
        state = StateEnum(d.pop("state"))

        def _parse_quoted_status(data: object) -> Union["Status", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                quoted_status_type_0 = Status.from_dict(data)

                return quoted_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Status", None, Unset], data)

        quoted_status = _parse_quoted_status(d.pop("quoted_status", UNSET))

        quote = cls(
            state=state,
            quoted_status=quoted_status,
        )

        quote.additional_properties = d
        return quote

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
