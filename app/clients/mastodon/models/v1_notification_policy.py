from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.v1_notification_policy_summary import \
        V1NotificationPolicySummary


T = TypeVar("T", bound="V1NotificationPolicy")


@_attrs_define
class V1NotificationPolicy:
    """Represents the notification filtering policy of the user.

    Example:
        {'filter_not_following': False, 'filter_not_followers': False, 'filter_new_accounts': False,
            'filter_private_mentions': True, 'summary': {'pending_requests_count': 0, 'pending_notifications_count': 0}}

    Attributes:
        filter_new_accounts (bool): Whether to filter notifications from accounts created in the past 30 days.
        filter_not_followers (bool): Whether to filter notifications from accounts that are not following the user.
        filter_not_following (bool): Whether to filter notifications from accounts the user is not following.
        filter_private_mentions (bool): Whether to filter notifications from private mentions. Replies to private
            mentions initiated by the user, as well as accounts the user follows, are never filtered.
        summary (V1NotificationPolicySummary): Summary of the filtered notifications
    """

    filter_new_accounts: bool
    filter_not_followers: bool
    filter_not_following: bool
    filter_private_mentions: bool
    summary: "V1NotificationPolicySummary"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filter_new_accounts = self.filter_new_accounts

        filter_not_followers = self.filter_not_followers

        filter_not_following = self.filter_not_following

        filter_private_mentions = self.filter_private_mentions

        summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filter_new_accounts": filter_new_accounts,
                "filter_not_followers": filter_not_followers,
                "filter_not_following": filter_not_following,
                "filter_private_mentions": filter_private_mentions,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.v1_notification_policy_summary import \
            V1NotificationPolicySummary

        d = src_dict.copy()
        filter_new_accounts = d.pop("filter_new_accounts")

        filter_not_followers = d.pop("filter_not_followers")

        filter_not_following = d.pop("filter_not_following")

        filter_private_mentions = d.pop("filter_private_mentions")

        summary = V1NotificationPolicySummary.from_dict(d.pop("summary"))

        v1_notification_policy = cls(
            filter_new_accounts=filter_new_accounts,
            filter_not_followers=filter_not_followers,
            filter_not_following=filter_not_following,
            filter_private_mentions=filter_private_mentions,
            summary=summary,
        )

        v1_notification_policy.additional_properties = d
        return v1_notification_policy

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
