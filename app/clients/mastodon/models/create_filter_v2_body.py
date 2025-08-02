from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_context import FilterContext
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_filter_v2_body_keywords_attributes_item import (
        CreateFilterV2BodyKeywordsAttributesItem,
    )


T = TypeVar("T", bound="CreateFilterV2Body")


@_attrs_define
class CreateFilterV2Body:
    """
    Attributes:
        context (list[FilterContext]): Where the filter should be applied. Specify at least one of `home`,
            `notifications`, `public`, `thread`, `account`.
        title (str): The name of the filter group.
        expires_in (Union[Unset, int]): How many seconds from now should the filter expire?
        filter_action (Union[Unset, str]): The policy to be applied when the filter is matched. Specify `warn`, `hide`
            or `blur`.
        keywords_attributes (Union[Unset, list['CreateFilterV2BodyKeywordsAttributesItem']]): Array of objects with
            properties: keyword, whole_word, id, _destroy
    """

    context: list[FilterContext]
    title: str
    expires_in: Union[Unset, int] = UNSET
    filter_action: Union[Unset, str] = UNSET
    keywords_attributes: Union[
        Unset, list["CreateFilterV2BodyKeywordsAttributesItem"]
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context = []
        for context_item_data in self.context:
            context_item = context_item_data.value
            context.append(context_item)

        title = self.title

        expires_in = self.expires_in

        filter_action = self.filter_action

        keywords_attributes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.keywords_attributes, Unset):
            keywords_attributes = []
            for keywords_attributes_item_data in self.keywords_attributes:
                keywords_attributes_item = keywords_attributes_item_data.to_dict()
                keywords_attributes.append(keywords_attributes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "title": title,
            }
        )
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if filter_action is not UNSET:
            field_dict["filter_action"] = filter_action
        if keywords_attributes is not UNSET:
            field_dict["keywords_attributes"] = keywords_attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_filter_v2_body_keywords_attributes_item import (
            CreateFilterV2BodyKeywordsAttributesItem,
        )

        d = src_dict.copy()
        context = []
        _context = d.pop("context")
        for context_item_data in _context:
            context_item = FilterContext(context_item_data)

            context.append(context_item)

        title = d.pop("title")

        expires_in = d.pop("expires_in", UNSET)

        filter_action = d.pop("filter_action", UNSET)

        keywords_attributes = []
        _keywords_attributes = d.pop("keywords_attributes", UNSET)
        for keywords_attributes_item_data in _keywords_attributes or []:
            keywords_attributes_item = (
                CreateFilterV2BodyKeywordsAttributesItem.from_dict(
                    keywords_attributes_item_data
                )
            )

            keywords_attributes.append(keywords_attributes_item)

        create_filter_v2_body = cls(
            context=context,
            title=title,
            expires_in=expires_in,
            filter_action=filter_action,
            keywords_attributes=keywords_attributes,
        )

        create_filter_v2_body.additional_properties = d
        return create_filter_v2_body

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
