import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.credential_account_source import CredentialAccountSource
    from ..models.custom_emoji import CustomEmoji
    from ..models.field import Field
    from ..models.role import Role


T = TypeVar("T", bound="CredentialAccount")


@_attrs_define
class CredentialAccount:
    """Additional entity definition for CredentialAccount

    Attributes:
        acct (str): The Webfinger account URI. Equal to `username` for local users, or `username@domain` for remote
            users.
        avatar (str): An image icon that is shown next to statuses and in the profile.
        avatar_static (str): A static version of the avatar. Equal to `avatar` if its value is a static image; different
            if `avatar` is an animated GIF.
        bot (bool): Indicates that the account may perform automated actions, may not be monitored, or identifies as a
            robot.
        created_at (datetime.datetime): When the account was created.
        display_name (str): The profile's display name.
        emojis (list['CustomEmoji']): Custom emoji entities to be used when rendering the profile.
        fields (list['Field']): Additional metadata attached to a profile as name-value pairs.
        followers_count (int): The reported followers of this profile.
        following_count (int): The reported follows of this profile.
        group (bool): Indicates that the account represents a Group actor.
        header (str): An image banner that is shown above the profile and in profile cards. Will end
            `/headers/original/missing.png` if the user has not set a header image.
        header_static (str): A static version of the header. Equal to `header` if its value is a static image; different
            if `header` is an animated GIF.
        id (str): The account id.
        locked (bool): Whether the account manually approves follow requests.
        note (str): The profile's bio or description.
        role (Role): Represents a custom user role that grants permissions. Example: {'id': '3', 'name': 'Owner',
            'color': '#ff3838', 'permissions': '1048575', 'highlighted': True}.
        source (CredentialAccountSource): An extra attribute that contains source values to be used with API methods
            that [verify credentials]({{< relref "methods/accounts#verify_credentials" >}}) and [update credentials]({{<
            relref "methods/accounts#update_credentials" >}}).
        statuses_count (int): How many statuses are attached to this account.
        uri (str): The user's ActivityPub actor identifier.
        url (str): The location of the user's profile page.
        username (str): The username of the account, not including domain.
        discoverable (Union[None, Unset, bool]): Whether the account has opted into discovery features such as the
            profile directory.
        hide_collections (Union[None, Unset, bool]): Whether the user hides the contents of their follows and followers
            collections.
        last_status_at (Union[None, Unset, datetime.date]): When the most recent status was posted.
        limited (Union[None, Unset, bool]): An extra attribute returned only when an account is silenced. If true,
            indicates that the account should be hidden behind a warning screen.
        moved (Union['Account', None, Unset]): Indicates that the profile is currently inactive and that its user has
            moved to a new account.
        noindex (Union[None, Unset, bool]): Whether the local user has opted out of being indexed by search engines.
        suspended (Union[None, Unset, bool]): An extra attribute returned only when an account is suspended.
    """

    acct: str
    avatar: str
    avatar_static: str
    bot: bool
    created_at: datetime.datetime
    display_name: str
    emojis: list["CustomEmoji"]
    fields: list["Field"]
    followers_count: int
    following_count: int
    group: bool
    header: str
    header_static: str
    id: str
    locked: bool
    note: str
    role: "Role"
    source: "CredentialAccountSource"
    statuses_count: int
    uri: str
    url: str
    username: str
    discoverable: Union[None, Unset, bool] = UNSET
    hide_collections: Union[None, Unset, bool] = UNSET
    last_status_at: Union[None, Unset, datetime.date] = UNSET
    limited: Union[None, Unset, bool] = UNSET
    moved: Union["Account", None, Unset] = UNSET
    noindex: Union[None, Unset, bool] = UNSET
    suspended: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account import Account

        acct = self.acct

        avatar = self.avatar

        avatar_static = self.avatar_static

        bot = self.bot

        created_at = self.created_at.isoformat()

        display_name = self.display_name

        emojis = []
        for emojis_item_data in self.emojis:
            emojis_item = emojis_item_data.to_dict()
            emojis.append(emojis_item)

        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            fields.append(fields_item)

        followers_count = self.followers_count

        following_count = self.following_count

        group = self.group

        header = self.header

        header_static = self.header_static

        id = self.id

        locked = self.locked

        note = self.note

        role = self.role.to_dict()

        source = self.source.to_dict()

        statuses_count = self.statuses_count

        uri = self.uri

        url = self.url

        username = self.username

        discoverable: Union[None, Unset, bool]
        if isinstance(self.discoverable, Unset):
            discoverable = UNSET
        else:
            discoverable = self.discoverable

        hide_collections: Union[None, Unset, bool]
        if isinstance(self.hide_collections, Unset):
            hide_collections = UNSET
        else:
            hide_collections = self.hide_collections

        last_status_at: Union[None, Unset, str]
        if isinstance(self.last_status_at, Unset):
            last_status_at = UNSET
        elif isinstance(self.last_status_at, datetime.date):
            last_status_at = self.last_status_at.isoformat()
        else:
            last_status_at = self.last_status_at

        limited: Union[None, Unset, bool]
        if isinstance(self.limited, Unset):
            limited = UNSET
        else:
            limited = self.limited

        moved: Union[None, Unset, dict[str, Any]]
        if isinstance(self.moved, Unset):
            moved = UNSET
        elif isinstance(self.moved, Account):
            moved = self.moved.to_dict()
        else:
            moved = self.moved

        noindex: Union[None, Unset, bool]
        if isinstance(self.noindex, Unset):
            noindex = UNSET
        else:
            noindex = self.noindex

        suspended: Union[None, Unset, bool]
        if isinstance(self.suspended, Unset):
            suspended = UNSET
        else:
            suspended = self.suspended

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "acct": acct,
                "avatar": avatar,
                "avatar_static": avatar_static,
                "bot": bot,
                "created_at": created_at,
                "display_name": display_name,
                "emojis": emojis,
                "fields": fields,
                "followers_count": followers_count,
                "following_count": following_count,
                "group": group,
                "header": header,
                "header_static": header_static,
                "id": id,
                "locked": locked,
                "note": note,
                "role": role,
                "source": source,
                "statuses_count": statuses_count,
                "uri": uri,
                "url": url,
                "username": username,
            }
        )
        if discoverable is not UNSET:
            field_dict["discoverable"] = discoverable
        if hide_collections is not UNSET:
            field_dict["hide_collections"] = hide_collections
        if last_status_at is not UNSET:
            field_dict["last_status_at"] = last_status_at
        if limited is not UNSET:
            field_dict["limited"] = limited
        if moved is not UNSET:
            field_dict["moved"] = moved
        if noindex is not UNSET:
            field_dict["noindex"] = noindex
        if suspended is not UNSET:
            field_dict["suspended"] = suspended

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.account import Account
        from ..models.credential_account_source import CredentialAccountSource
        from ..models.custom_emoji import CustomEmoji
        from ..models.field import Field
        from ..models.role import Role

        d = src_dict.copy()
        acct = d.pop("acct")

        avatar = d.pop("avatar")

        avatar_static = d.pop("avatar_static")

        bot = d.pop("bot")

        created_at = isoparse(d.pop("created_at"))

        display_name = d.pop("display_name")

        emojis = []
        _emojis = d.pop("emojis")
        for emojis_item_data in _emojis:
            emojis_item = CustomEmoji.from_dict(emojis_item_data)

            emojis.append(emojis_item)

        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = Field.from_dict(fields_item_data)

            fields.append(fields_item)

        followers_count = d.pop("followers_count")

        following_count = d.pop("following_count")

        group = d.pop("group")

        header = d.pop("header")

        header_static = d.pop("header_static")

        id = d.pop("id")

        locked = d.pop("locked")

        note = d.pop("note")

        role = Role.from_dict(d.pop("role"))

        source = CredentialAccountSource.from_dict(d.pop("source"))

        statuses_count = d.pop("statuses_count")

        uri = d.pop("uri")

        url = d.pop("url")

        username = d.pop("username")

        def _parse_discoverable(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        discoverable = _parse_discoverable(d.pop("discoverable", UNSET))

        def _parse_hide_collections(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        hide_collections = _parse_hide_collections(d.pop("hide_collections", UNSET))

        def _parse_last_status_at(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_status_at_type_0 = isoparse(data).date()

                return last_status_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        last_status_at = _parse_last_status_at(d.pop("last_status_at", UNSET))

        def _parse_limited(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        limited = _parse_limited(d.pop("limited", UNSET))

        def _parse_moved(data: object) -> Union["Account", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                moved_type_0 = Account.from_dict(data)

                return moved_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Account", None, Unset], data)

        moved = _parse_moved(d.pop("moved", UNSET))

        def _parse_noindex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        noindex = _parse_noindex(d.pop("noindex", UNSET))

        def _parse_suspended(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        suspended = _parse_suspended(d.pop("suspended", UNSET))

        credential_account = cls(
            acct=acct,
            avatar=avatar,
            avatar_static=avatar_static,
            bot=bot,
            created_at=created_at,
            display_name=display_name,
            emojis=emojis,
            fields=fields,
            followers_count=followers_count,
            following_count=following_count,
            group=group,
            header=header,
            header_static=header_static,
            id=id,
            locked=locked,
            note=note,
            role=role,
            source=source,
            statuses_count=statuses_count,
            uri=uri,
            url=url,
            username=username,
            discoverable=discoverable,
            hide_collections=hide_collections,
            last_status_at=last_status_at,
            limited=limited,
            moved=moved,
            noindex=noindex,
            suspended=suspended,
        )

        credential_account.additional_properties = d
        return credential_account

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
