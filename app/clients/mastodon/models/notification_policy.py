from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.notification_policy_summary import NotificationPolicySummary


T = TypeVar("T", bound="NotificationPolicy")


@_attrs_define
class NotificationPolicy:
    """Represents the notification filtering policy of the user.

    Example:
        {'for_not_following': 'accept', 'for_not_followers': 'accept', 'for_new_accounts': 'accept',
            'for_private_mentions': 'drop', 'for_limited_accounts': 'filter', 'summary': {'pending_requests_count': 0,
            'pending_notifications_count': 0}}

    Attributes:
        for_limited_accounts (str): Whether to `accept`, `filter` or `drop` notifications from accounts that were
            limited by a moderator. `drop` will prevent creation of the notification object altogether (without preventing
            the underlying activity), `filter` will cause it to be marked as filtered, and `accept` will not affect its
            processing.
        for_new_accounts (str): Whether to `accept`, `filter` or `drop` notifications from accounts created in the past
            30 days. `drop` will prevent creation of the notification object altogether (without preventing the underlying
            activity), `filter` will cause it to be marked as filtered, and `accept` will not affect its processing.
        for_not_followers (str): Whether to `accept`, `filter` or `drop` notifications from accounts that are not
            following the user. `drop` will prevent creation of the notification object altogether (without preventing the
            underlying activity), `filter` will cause it to be marked as filtered, and `accept` will not affect its
            processing.
        for_not_following (str): Whether to `accept`, `filter` or `drop` notifications from accounts the user is not
            following. `drop` will prevent creation of the notification object altogether (without preventing the underlying
            activity), `filter` will cause it to be marked as filtered, and `accept` will not affect its processing.
        for_private_mentions (str): Whether to `accept`, `filter` or `drop` notifications from private mentions. `drop`
            will prevent creation of the notification object altogether (without preventing the underlying activity),
            `filter` will cause it to be marked as filtered, and `accept` will not affect its processing. Replies to private
            mentions initiated by the user, as well as accounts the user follows, are always allowed, regardless of this
            value.
        summary (NotificationPolicySummary): Summary of the filtered notifications
    """

    for_limited_accounts: str
    for_new_accounts: str
    for_not_followers: str
    for_not_following: str
    for_private_mentions: str
    summary: "NotificationPolicySummary"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        for_limited_accounts = self.for_limited_accounts

        for_new_accounts = self.for_new_accounts

        for_not_followers = self.for_not_followers

        for_not_following = self.for_not_following

        for_private_mentions = self.for_private_mentions

        summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "for_limited_accounts": for_limited_accounts,
                "for_new_accounts": for_new_accounts,
                "for_not_followers": for_not_followers,
                "for_not_following": for_not_following,
                "for_private_mentions": for_private_mentions,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.notification_policy_summary import NotificationPolicySummary

        d = src_dict.copy()
        for_limited_accounts = d.pop("for_limited_accounts")

        for_new_accounts = d.pop("for_new_accounts")

        for_not_followers = d.pop("for_not_followers")

        for_not_following = d.pop("for_not_following")

        for_private_mentions = d.pop("for_private_mentions")

        summary = NotificationPolicySummary.from_dict(d.pop("summary"))

        notification_policy = cls(
            for_limited_accounts=for_limited_accounts,
            for_new_accounts=for_new_accounts,
            for_not_followers=for_not_followers,
            for_not_following=for_not_following,
            for_private_mentions=for_private_mentions,
            summary=summary,
        )

        notification_policy.additional_properties = d
        return notification_policy

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
