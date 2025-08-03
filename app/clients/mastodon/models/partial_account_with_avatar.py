from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PartialAccountWithAvatar")


@_attrs_define
class PartialAccountWithAvatar:
    """These are stripped-down versions of [Account]({{< relref "entities/Account" >}}) that only contain what is necessary
    to display a list of avatars, as well as a few other useful properties. The aim is to cut back on expensive server-
    side serialization and reduce the network payload size of notification groups.

    Attributes:
            acct (str): The Webfinger account URI. Equal to `username` for local users, or `username@domain` for remote
                users.
            avatar (str): An image icon that is shown next to statuses and in the profile.
            avatar_static (str): A static version of the avatar. Equal to `avatar` if its value is a static image; different
                if `avatar` is an animated GIF.
            bot (bool): Indicates that the account may perform automated actions, may not be monitored, or identifies as a
                robot.
            id (str): The account id.
            locked (bool): Whether the account manually approves follow requests.
            url (str): The location of the user's profile page.

    """

    acct: str
    avatar: str
    avatar_static: str
    bot: bool
    id: str
    locked: bool
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        acct = self.acct

        avatar = self.avatar

        avatar_static = self.avatar_static

        bot = self.bot

        id = self.id

        locked = self.locked

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "acct": acct,
                "avatar": avatar,
                "avatar_static": avatar_static,
                "bot": bot,
                "id": id,
                "locked": locked,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        acct = d.pop("acct")

        avatar = d.pop("avatar")

        avatar_static = d.pop("avatar_static")

        bot = d.pop("bot")

        id = d.pop("id")

        locked = d.pop("locked")

        url = d.pop("url")

        partial_account_with_avatar = cls(
            acct=acct,
            avatar=avatar,
            avatar_static=avatar_static,
            bot=bot,
            id=id,
            locked=locked,
            url=url,
        )

        partial_account_with_avatar.additional_properties = d
        return partial_account_with_avatar

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
