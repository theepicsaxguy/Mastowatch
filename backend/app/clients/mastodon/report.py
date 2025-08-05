import datetime
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
from dateutil.parser import isoparse

from ..models.category_enum import CategoryEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account


T = TypeVar("T", bound="Report")


@_attrs_define
class Report:
    """Reports filed against users and/or statuses, to be taken action on by moderators.

    Attributes:
        action_taken (bool): Whether an action was taken yet.
        category (CategoryEnum):
        comment (str): The reason for the report.
        created_at (datetime.datetime): When the report was created.
        forwarded (bool): Whether the report was forwarded to a remote domain.
        id (str): The ID of the report in the database.
        target_account (Account): Represents a user of Mastodon and their associated profile.
        action_taken_at (Union[None, Unset, datetime.datetime]): When an action was taken against the report.
        rule_ids (Union[None, Unset, list[str]]): IDs of the rules that have been cited as a violation by this report.
        status_ids (Union[None, Unset, list[str]]): IDs of statuses that have been attached to this report for
            additional context.
    """

    action_taken: bool
    category: CategoryEnum
    comment: str
    created_at: datetime.datetime
    forwarded: bool
    id: str
    target_account: "Account"
    action_taken_at: Union[None, Unset, datetime.datetime] = UNSET
    rule_ids: Union[None, Unset, list[str]] = UNSET
    status_ids: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_taken = self.action_taken

        category = self.category.value

        comment = self.comment

        created_at = self.created_at.isoformat()

        forwarded = self.forwarded

        id = self.id

        target_account = self.target_account.to_dict()

        action_taken_at: Union[None, Unset, str]
        if isinstance(self.action_taken_at, Unset):
            action_taken_at = UNSET
        elif isinstance(self.action_taken_at, datetime.datetime):
            action_taken_at = self.action_taken_at.isoformat()
        else:
            action_taken_at = self.action_taken_at

        rule_ids: Union[None, Unset, list[str]]
        if isinstance(self.rule_ids, Unset):
            rule_ids = UNSET
        elif isinstance(self.rule_ids, list):
            rule_ids = self.rule_ids

        else:
            rule_ids = self.rule_ids

        status_ids: Union[None, Unset, list[str]]
        if isinstance(self.status_ids, Unset):
            status_ids = UNSET
        elif isinstance(self.status_ids, list):
            status_ids = self.status_ids

        else:
            status_ids = self.status_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action_taken": action_taken,
                "category": category,
                "comment": comment,
                "created_at": created_at,
                "forwarded": forwarded,
                "id": id,
                "target_account": target_account,
            }
        )
        if action_taken_at is not UNSET:
            field_dict["action_taken_at"] = action_taken_at
        if rule_ids is not UNSET:
            field_dict["rule_ids"] = rule_ids
        if status_ids is not UNSET:
            field_dict["status_ids"] = status_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account

        d = dict(src_dict)
        action_taken = d.pop("action_taken")

        category = CategoryEnum(d.pop("category"))

        comment = d.pop("comment")

        created_at = isoparse(d.pop("created_at"))

        forwarded = d.pop("forwarded")

        id = d.pop("id")

        target_account = Account.from_dict(d.pop("target_account"))

        def _parse_action_taken_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_taken_at_type_0 = isoparse(data)

                return action_taken_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_taken_at = _parse_action_taken_at(d.pop("action_taken_at", UNSET))

        def _parse_rule_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                rule_ids_type_0 = cast(list[str], data)

                return rule_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        rule_ids = _parse_rule_ids(d.pop("rule_ids", UNSET))

        def _parse_status_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                status_ids_type_0 = cast(list[str], data)

                return status_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        status_ids = _parse_status_ids(d.pop("status_ids", UNSET))

        report = cls(
            action_taken=action_taken,
            category=category,
            comment=comment,
            created_at=created_at,
            forwarded=forwarded,
            id=id,
            target_account=target_account,
            action_taken_at=action_taken_at,
            rule_ids=rule_ids,
            status_ids=status_ids,
        )

        report.additional_properties = d
        return report

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
