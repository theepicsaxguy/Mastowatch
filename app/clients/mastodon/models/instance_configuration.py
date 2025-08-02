from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_configuration_accounts import \
        InstanceConfigurationAccounts
    from ..models.instance_configuration_media_attachments import \
        InstanceConfigurationMediaAttachments
    from ..models.instance_configuration_polls import \
        InstanceConfigurationPolls
    from ..models.instance_configuration_statuses import \
        InstanceConfigurationStatuses
    from ..models.instance_configuration_translation import \
        InstanceConfigurationTranslation
    from ..models.instance_configuration_urls import InstanceConfigurationUrls


T = TypeVar("T", bound="InstanceConfiguration")


@_attrs_define
class InstanceConfiguration:
    """Configured values and limits for this website.

    Attributes:
        accounts (InstanceConfigurationAccounts): Limits related to accounts.
        limited_federation (bool): Whether federation is limited to explicitly allowed domains.
        media_attachments (InstanceConfigurationMediaAttachments): Hints for which attachments will be accepted.
        polls (InstanceConfigurationPolls): Limits related to polls.
        statuses (InstanceConfigurationStatuses): Limits related to authoring statuses.
        translation (InstanceConfigurationTranslation): Hints related to translation.
        urls (InstanceConfigurationUrls): URLs of interest for clients apps.
    """

    accounts: "InstanceConfigurationAccounts"
    limited_federation: bool
    media_attachments: "InstanceConfigurationMediaAttachments"
    polls: "InstanceConfigurationPolls"
    statuses: "InstanceConfigurationStatuses"
    translation: "InstanceConfigurationTranslation"
    urls: "InstanceConfigurationUrls"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts.to_dict()

        limited_federation = self.limited_federation

        media_attachments = self.media_attachments.to_dict()

        polls = self.polls.to_dict()

        statuses = self.statuses.to_dict()

        translation = self.translation.to_dict()

        urls = self.urls.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "limited_federation": limited_federation,
                "media_attachments": media_attachments,
                "polls": polls,
                "statuses": statuses,
                "translation": translation,
                "urls": urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.instance_configuration_accounts import \
            InstanceConfigurationAccounts
        from ..models.instance_configuration_media_attachments import \
            InstanceConfigurationMediaAttachments
        from ..models.instance_configuration_polls import \
            InstanceConfigurationPolls
        from ..models.instance_configuration_statuses import \
            InstanceConfigurationStatuses
        from ..models.instance_configuration_translation import \
            InstanceConfigurationTranslation
        from ..models.instance_configuration_urls import \
            InstanceConfigurationUrls

        d = src_dict.copy()
        accounts = InstanceConfigurationAccounts.from_dict(d.pop("accounts"))

        limited_federation = d.pop("limited_federation")

        media_attachments = InstanceConfigurationMediaAttachments.from_dict(d.pop("media_attachments"))

        polls = InstanceConfigurationPolls.from_dict(d.pop("polls"))

        statuses = InstanceConfigurationStatuses.from_dict(d.pop("statuses"))

        translation = InstanceConfigurationTranslation.from_dict(d.pop("translation"))

        urls = InstanceConfigurationUrls.from_dict(d.pop("urls"))

        instance_configuration = cls(
            accounts=accounts,
            limited_federation=limited_federation,
            media_attachments=media_attachments,
            polls=polls,
            statuses=statuses,
            translation=translation,
            urls=urls,
        )

        instance_configuration.additional_properties = d
        return instance_configuration

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
