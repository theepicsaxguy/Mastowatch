from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_accounts_update_credentials_body_fields_attributes import \
        PatchAccountsUpdateCredentialsBodyFieldsAttributes
    from ..models.patch_accounts_update_credentials_body_source import \
        PatchAccountsUpdateCredentialsBodySource


T = TypeVar("T", bound="PatchAccountsUpdateCredentialsBody")


@_attrs_define
class PatchAccountsUpdateCredentialsBody:
    """
    Attributes:
        attribution_domains (Union[Unset, list[str]]): Domains of websites allowed to credit the account.
        avatar (Union[Unset, str]): Avatar image encoded using `multipart/form-data`
        bot (Union[Unset, bool]): Whether the account has a bot flag.
        discoverable (Union[Unset, bool]): Whether the account should be shown in the profile directory.
        display_name (Union[Unset, str]): The display name to use for the profile.
        fields_attributes (Union[Unset, PatchAccountsUpdateCredentialsBodyFieldsAttributes]): The profile fields to be
            set. Inside this hash, the key is an integer cast to a string (although the exact integer does not matter), and
            the value is another hash including `name` and `value`. By default, max 4 fields.
        header (Union[Unset, str]): Header image encoded using `multipart/form-data`
        hide_collections (Union[Unset, bool]): Whether to hide followers and followed accounts.
        indexable (Union[Unset, bool]): Whether public posts should be searchable to anyone.
        locked (Union[Unset, bool]): Whether manual approval of follow requests is required.
        note (Union[Unset, str]): The account bio.
        source (Union[Unset, PatchAccountsUpdateCredentialsBodySource]): Object containing properties
    """

    attribution_domains: Union[Unset, list[str]] = UNSET
    avatar: Union[Unset, str] = UNSET
    bot: Union[Unset, bool] = UNSET
    discoverable: Union[Unset, bool] = UNSET
    display_name: Union[Unset, str] = UNSET
    fields_attributes: Union[Unset, "PatchAccountsUpdateCredentialsBodyFieldsAttributes"] = UNSET
    header: Union[Unset, str] = UNSET
    hide_collections: Union[Unset, bool] = UNSET
    indexable: Union[Unset, bool] = UNSET
    locked: Union[Unset, bool] = UNSET
    note: Union[Unset, str] = UNSET
    source: Union[Unset, "PatchAccountsUpdateCredentialsBodySource"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribution_domains: Union[Unset, list[str]] = UNSET
        if not isinstance(self.attribution_domains, Unset):
            attribution_domains = self.attribution_domains

        avatar = self.avatar

        bot = self.bot

        discoverable = self.discoverable

        display_name = self.display_name

        fields_attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields_attributes, Unset):
            fields_attributes = self.fields_attributes.to_dict()

        header = self.header

        hide_collections = self.hide_collections

        indexable = self.indexable

        locked = self.locked

        note = self.note

        source: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attribution_domains is not UNSET:
            field_dict["attribution_domains"] = attribution_domains
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if bot is not UNSET:
            field_dict["bot"] = bot
        if discoverable is not UNSET:
            field_dict["discoverable"] = discoverable
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if fields_attributes is not UNSET:
            field_dict["fields_attributes"] = fields_attributes
        if header is not UNSET:
            field_dict["header"] = header
        if hide_collections is not UNSET:
            field_dict["hide_collections"] = hide_collections
        if indexable is not UNSET:
            field_dict["indexable"] = indexable
        if locked is not UNSET:
            field_dict["locked"] = locked
        if note is not UNSET:
            field_dict["note"] = note
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.patch_accounts_update_credentials_body_fields_attributes import \
            PatchAccountsUpdateCredentialsBodyFieldsAttributes
        from ..models.patch_accounts_update_credentials_body_source import \
            PatchAccountsUpdateCredentialsBodySource

        d = src_dict.copy()
        attribution_domains = cast(list[str], d.pop("attribution_domains", UNSET))

        avatar = d.pop("avatar", UNSET)

        bot = d.pop("bot", UNSET)

        discoverable = d.pop("discoverable", UNSET)

        display_name = d.pop("display_name", UNSET)

        _fields_attributes = d.pop("fields_attributes", UNSET)
        fields_attributes: Union[Unset, PatchAccountsUpdateCredentialsBodyFieldsAttributes]
        if isinstance(_fields_attributes, Unset):
            fields_attributes = UNSET
        else:
            fields_attributes = PatchAccountsUpdateCredentialsBodyFieldsAttributes.from_dict(_fields_attributes)

        header = d.pop("header", UNSET)

        hide_collections = d.pop("hide_collections", UNSET)

        indexable = d.pop("indexable", UNSET)

        locked = d.pop("locked", UNSET)

        note = d.pop("note", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, PatchAccountsUpdateCredentialsBodySource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = PatchAccountsUpdateCredentialsBodySource.from_dict(_source)

        patch_accounts_update_credentials_body = cls(
            attribution_domains=attribution_domains,
            avatar=avatar,
            bot=bot,
            discoverable=discoverable,
            display_name=display_name,
            fields_attributes=fields_attributes,
            header=header,
            hide_collections=hide_collections,
            indexable=indexable,
            locked=locked,
            note=note,
            source=source,
        )

        patch_accounts_update_credentials_body.additional_properties = d
        return patch_accounts_update_credentials_body

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
