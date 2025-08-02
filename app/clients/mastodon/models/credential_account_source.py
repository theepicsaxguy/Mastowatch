from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.credential_account_source_privacy import CredentialAccountSourcePrivacy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field import Field


T = TypeVar("T", bound="CredentialAccountSource")


@_attrs_define
class CredentialAccountSource:
    """An extra attribute that contains source values to be used with API methods that [verify credentials]({{< relref
    "methods/accounts#verify_credentials" >}}) and [update credentials]({{< relref "methods/accounts#update_credentials"
    >}}).

        Attributes:
            attribution_domains (list[str]): Domains of websites allowed to credit the account.
            fields (list['Field']): Metadata about the account.
            follow_requests_count (int): The number of pending follow requests.
            note (str): Profile bio, in plain-text instead of in HTML.
            privacy (CredentialAccountSourcePrivacy): The default post privacy to be used for new statuses.
            sensitive (bool): Whether new statuses should be marked sensitive by default.
            language (Union[None, Unset, str]): The default posting language for new statuses.
    """

    attribution_domains: list[str]
    fields: list["Field"]
    follow_requests_count: int
    note: str
    privacy: CredentialAccountSourcePrivacy
    sensitive: bool
    language: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribution_domains = self.attribution_domains

        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()
            fields.append(fields_item)

        follow_requests_count = self.follow_requests_count

        note = self.note

        privacy = self.privacy.value

        sensitive = self.sensitive

        language: Union[None, Unset, str]
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attribution_domains": attribution_domains,
                "fields": fields,
                "follow_requests_count": follow_requests_count,
                "note": note,
                "privacy": privacy,
                "sensitive": sensitive,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.field import Field

        d = src_dict.copy()
        attribution_domains = cast(list[str], d.pop("attribution_domains"))

        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = Field.from_dict(fields_item_data)

            fields.append(fields_item)

        follow_requests_count = d.pop("follow_requests_count")

        note = d.pop("note")

        privacy = CredentialAccountSourcePrivacy(d.pop("privacy"))

        sensitive = d.pop("sensitive")

        def _parse_language(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        language = _parse_language(d.pop("language", UNSET))

        credential_account_source = cls(
            attribution_domains=attribution_domains,
            fields=fields,
            follow_requests_count=follow_requests_count,
            note=note,
            privacy=privacy,
            sensitive=sensitive,
            language=language,
        )

        credential_account_source.additional_properties = d
        return credential_account_source

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
