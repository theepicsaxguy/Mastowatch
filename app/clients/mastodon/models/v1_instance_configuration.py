from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.v1_instance_configuration_accounts import (
        V1InstanceConfigurationAccounts,
    )
    from ..models.v1_instance_configuration_media_attachments import (
        V1InstanceConfigurationMediaAttachments,
    )
    from ..models.v1_instance_configuration_polls import V1InstanceConfigurationPolls
    from ..models.v1_instance_configuration_statuses import (
        V1InstanceConfigurationStatuses,
    )


T = TypeVar("T", bound="V1InstanceConfiguration")


@_attrs_define
class V1InstanceConfiguration:
    """Configured values and limits for this website.

    Attributes:
        accounts (V1InstanceConfigurationAccounts): Limits related to accounts.
        media_attachments (V1InstanceConfigurationMediaAttachments): Hints for which attachments will be accepted.
        polls (V1InstanceConfigurationPolls): Limits related to polls.
        statuses (V1InstanceConfigurationStatuses): Limits related to authoring statuses.
    """

    accounts: "V1InstanceConfigurationAccounts"
    media_attachments: "V1InstanceConfigurationMediaAttachments"
    polls: "V1InstanceConfigurationPolls"
    statuses: "V1InstanceConfigurationStatuses"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accounts = self.accounts.to_dict()

        media_attachments = self.media_attachments.to_dict()

        polls = self.polls.to_dict()

        statuses = self.statuses.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accounts": accounts,
                "media_attachments": media_attachments,
                "polls": polls,
                "statuses": statuses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.v1_instance_configuration_accounts import (
            V1InstanceConfigurationAccounts,
        )
        from ..models.v1_instance_configuration_media_attachments import (
            V1InstanceConfigurationMediaAttachments,
        )
        from ..models.v1_instance_configuration_polls import (
            V1InstanceConfigurationPolls,
        )
        from ..models.v1_instance_configuration_statuses import (
            V1InstanceConfigurationStatuses,
        )

        d = src_dict.copy()
        accounts = V1InstanceConfigurationAccounts.from_dict(d.pop("accounts"))

        media_attachments = V1InstanceConfigurationMediaAttachments.from_dict(
            d.pop("media_attachments")
        )

        polls = V1InstanceConfigurationPolls.from_dict(d.pop("polls"))

        statuses = V1InstanceConfigurationStatuses.from_dict(d.pop("statuses"))

        v1_instance_configuration = cls(
            accounts=accounts,
            media_attachments=media_attachments,
            polls=polls,
            statuses=statuses,
        )

        v1_instance_configuration.additional_properties = d
        return v1_instance_configuration

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
