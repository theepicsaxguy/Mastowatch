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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rule_translations_type_0 import RuleTranslationsType0


T = TypeVar("T", bound="Rule")


@_attrs_define
class Rule:
    r"""Represents a rule that server users should follow.

    Example:
        {'id': '2', 'text': 'No racism, sexism, homophobia, transphobia, ableism, xenophobia, or casteism.', 'hint':
            'Transphobic behavior such as intentional misgendering and deadnaming is strictly prohibited. Promotion of
            "conversion therapy" is strictly prohibited. Criticism of governments and religions is permissible unless being
            used as a proxy for discrimination.', 'translations': {'fr': {'text': 'Pas de racisme, sexisme, homophobie,
            transphobie, validisme, xénophobie ou casteisme.', 'hint': "Les comportements transhobes tels que le deadnaming
            intentionel sont formellement interdits. La promotion des «\xa0thérapies de conversion\xa0» est formellement
            interdite. La critique des gouvernements et des religions est permise à moins qu'elle ne soit utilisée comme
            excuse pour de la discrimination."}}}

    Attributes:
        hint (str): Longer-form description of the rule.
        id (str): An identifier for the rule.
        text (str): The rule to be followed.
        translations (Union['RuleTranslationsType0', None, Unset]): Available translations for this rule's `text` and
            `hint`, as a Hash where keys are locale codes and values are hashes with `text` and `hint` keys.
    """

    hint: str
    id: str
    text: str
    translations: Union["RuleTranslationsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rule_translations_type_0 import RuleTranslationsType0

        hint = self.hint

        id = self.id

        text = self.text

        translations: Union[None, Unset, dict[str, Any]]
        if isinstance(self.translations, Unset):
            translations = UNSET
        elif isinstance(self.translations, RuleTranslationsType0):
            translations = self.translations.to_dict()
        else:
            translations = self.translations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hint": hint,
                "id": id,
                "text": text,
            }
        )
        if translations is not UNSET:
            field_dict["translations"] = translations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rule_translations_type_0 import RuleTranslationsType0

        d = dict(src_dict)
        hint = d.pop("hint")

        id = d.pop("id")

        text = d.pop("text")

        def _parse_translations(
            data: object,
        ) -> Union["RuleTranslationsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                translations_type_0 = RuleTranslationsType0.from_dict(data)

                return translations_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RuleTranslationsType0", None, Unset], data)

        translations = _parse_translations(d.pop("translations", UNSET))

        rule = cls(
            hint=hint,
            id=id,
            text=text,
            translations=translations,
        )

        rule.additional_properties = d
        return rule

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
