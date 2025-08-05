from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_marker_body_home import CreateMarkerBodyHome
    from ..models.create_marker_body_notifications import CreateMarkerBodyNotifications


T = TypeVar("T", bound="CreateMarkerBody")


@_attrs_define
class CreateMarkerBody:
    """
    Attributes:
        home (Union[Unset, CreateMarkerBodyHome]): Object containing properties
        notifications (Union[Unset, CreateMarkerBodyNotifications]): Object containing properties
    """

    home: Union[Unset, "CreateMarkerBodyHome"] = UNSET
    notifications: Union[Unset, "CreateMarkerBodyNotifications"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        home: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.home, Unset):
            home = self.home.to_dict()

        notifications: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.notifications, Unset):
            notifications = self.notifications.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if home is not UNSET:
            field_dict["home"] = home
        if notifications is not UNSET:
            field_dict["notifications"] = notifications

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_marker_body_home import CreateMarkerBodyHome
        from ..models.create_marker_body_notifications import (
            CreateMarkerBodyNotifications,
        )

        d = dict(src_dict)
        _home = d.pop("home", UNSET)
        home: Union[Unset, CreateMarkerBodyHome]
        if isinstance(_home, Unset):
            home = UNSET
        else:
            home = CreateMarkerBodyHome.from_dict(_home)

        _notifications = d.pop("notifications", UNSET)
        notifications: Union[Unset, CreateMarkerBodyNotifications]
        if isinstance(_notifications, Unset):
            notifications = UNSET
        else:
            notifications = CreateMarkerBodyNotifications.from_dict(_notifications)

        create_marker_body = cls(
            home=home,
            notifications=notifications,
        )

        create_marker_body.additional_properties = d
        return create_marker_body

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
