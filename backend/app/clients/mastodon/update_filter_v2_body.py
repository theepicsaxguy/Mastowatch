from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_context import FilterContext
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_filter_v2_body_keywords_attributes_item import (
        UpdateFilterV2BodyKeywordsAttributesItem,
    )


T = TypeVar("T", bound="UpdateFilterV2Body")


@_attrs_define
class UpdateFilterV2Body:
    """
    Attributes:
        context (Union[Unset, list[FilterContext]]): Where the filter should be applied. Specify at least one of `home`,
            `notifications`, `public`, `thread`, `account`.
        expires_in (Union[Unset, int]): How many seconds from now should the filter expire?
        filter_action (Union[Unset, str]): The policy to be applied when the filter is matched. Specify `warn`, `hide`
            or `blur`.
        keywords_attributes (Union[Unset, list['UpdateFilterV2BodyKeywordsAttributesItem']]): Array of objects with
            properties: keyword, whole_word, id, _destroy
        title (Union[Unset, str]): The name of the filter group.
    """

    context: Union[Unset, list[FilterContext]] = UNSET
    expires_in: Union[Unset, int] = UNSET
    filter_action: Union[Unset, str] = UNSET
    keywords_attributes: Union[
        Unset, list["UpdateFilterV2BodyKeywordsAttributesItem"]
    ] = UNSET
    title: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context: Union[Unset, list[str]] = UNSET
        if not isinstance(self.context, Unset):
            context = []
            for context_item_data in self.context:
                context_item = context_item_data.value
                context.append(context_item)

        expires_in = self.expires_in

        filter_action = self.filter_action

        keywords_attributes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.keywords_attributes, Unset):
            keywords_attributes = []
            for keywords_attributes_item_data in self.keywords_attributes:
                keywords_attributes_item = keywords_attributes_item_data.to_dict()
                keywords_attributes.append(keywords_attributes_item)

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["context"] = context
        if expires_in is not UNSET:
            field_dict["expires_in"] = expires_in
        if filter_action is not UNSET:
            field_dict["filter_action"] = filter_action
        if keywords_attributes is not UNSET:
            field_dict["keywords_attributes"] = keywords_attributes
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_filter_v2_body_keywords_attributes_item import (
            UpdateFilterV2BodyKeywordsAttributesItem,
        )

        d = dict(src_dict)
        context = []
        _context = d.pop("context", UNSET)
        for context_item_data in _context or []:
            context_item = FilterContext(context_item_data)

            context.append(context_item)

        expires_in = d.pop("expires_in", UNSET)

        filter_action = d.pop("filter_action", UNSET)

        keywords_attributes = []
        _keywords_attributes = d.pop("keywords_attributes", UNSET)
        for keywords_attributes_item_data in _keywords_attributes or []:
            keywords_attributes_item = (
                UpdateFilterV2BodyKeywordsAttributesItem.from_dict(
                    keywords_attributes_item_data
                )
            )

            keywords_attributes.append(keywords_attributes_item)

        title = d.pop("title", UNSET)

        update_filter_v2_body = cls(
            context=context,
            expires_in=expires_in,
            filter_action=filter_action,
            keywords_attributes=keywords_attributes,
            title=title,
        )

        update_filter_v2_body.additional_properties = d
        return update_filter_v2_body

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
