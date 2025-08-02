from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_report_body_category import CreateReportBodyCategory
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateReportBody")


@_attrs_define
class CreateReportBody:
    """
    Attributes:
        account_id (str): ID of the account to report.
        category (Union[Unset, CreateReportBodyCategory]): Specify if the report is due to `spam`, `legal` (illegal
            content), `violation` of enumerated instance rules, or some `other` reason. Defaults to `other`. Will be set to
            `violation` if `rule_ids[]` is provided (regardless of any category value you provide). Default:
            CreateReportBodyCategory.OTHER.
        comment (Union[Unset, str]): The reason for the report. Default maximum of 1000 characters.
        forward (Union[Unset, bool]): If the account is remote, should the report be forwarded to the remote admin?
            Defaults to false. Default: False.
        rule_ids (Union[Unset, list[str]]): For `violation` category reports, specify the ID of the exact rules broken.
            Rules and their IDs are available via [GET /api/v1/instance/rules] and [GET /api/v1/instance]. See [Handling and
            sorting IDs] for more information.
        status_ids (Union[Unset, list[str]]): You can attach statuses to the report to provide additional context.
    """

    account_id: str
    category: Union[Unset, CreateReportBodyCategory] = CreateReportBodyCategory.OTHER
    comment: Union[Unset, str] = UNSET
    forward: Union[Unset, bool] = False
    rule_ids: Union[Unset, list[str]] = UNSET
    status_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_id = self.account_id

        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        comment = self.comment

        forward = self.forward

        rule_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.rule_ids, Unset):
            rule_ids = self.rule_ids

        status_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.status_ids, Unset):
            status_ids = self.status_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category
        if comment is not UNSET:
            field_dict["comment"] = comment
        if forward is not UNSET:
            field_dict["forward"] = forward
        if rule_ids is not UNSET:
            field_dict["rule_ids"] = rule_ids
        if status_ids is not UNSET:
            field_dict["status_ids"] = status_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("account_id")

        _category = d.pop("category", UNSET)
        category: Union[Unset, CreateReportBodyCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = CreateReportBodyCategory(_category)

        comment = d.pop("comment", UNSET)

        forward = d.pop("forward", UNSET)

        rule_ids = cast(list[str], d.pop("rule_ids", UNSET))

        status_ids = cast(list[str], d.pop("status_ids", UNSET))

        create_report_body = cls(
            account_id=account_id,
            category=category,
            comment=comment,
            forward=forward,
            rule_ids=rule_ids,
            status_ids=status_ids,
        )

        create_report_body.additional_properties = d
        return create_report_body

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
