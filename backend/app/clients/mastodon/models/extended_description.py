import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ExtendedDescription")


@_attrs_define
class ExtendedDescription:
    r"""Represents an extended description for the instance, to be shown on its about page.

    Example:
        {'updated_at': '2022-11-03T04:09:07Z', 'content': '<p>For inquiries not related specifically to the operation of
            this server, such as press inquiries, please contact <a
            href="mailto:press@joinmastodon.org">press@joinmastodon.org</a>.</p>\n\n<h2>Funding</h2>\n\n<p>This server is
            crowdfunded by <a href="https://patreon.com/mastodon">Patreon donations</a>. For a list of sponsors, see <a
            href="https://joinmastodon.org/sponsors">joinmastodon.org</a>.</p>\n\n<h2>Reporting and
            moderation</h2>\n\n<p>When reporting accounts, please make sure to include at least a few posts that show rule-
            breaking behaviour, when applicable. If there is any additional context that might help make a decision, please
            also include it in the comment. This is especially important when the content is in a language nobody on the
            moderation team speaks.</p>\n\n<p>We usually handle reports within 24 hours. Please mind that you are not
            notified when a report you have made has led to a punitive action, and that not all punitive actions are
            externally visible. For first time offenses, we may opt to delete offending content, escalating to harsher
            measures on repeat offenses.</p>\n\n<h2>Impressum</h2>\n\n<p>Mastodon gGmbH<br>\nMühlenstraße 8a<br>\n14167
            Berlin<br>\nGermany</p>\n\n<p>E-Mail-Adresse: hello@joinmastodon.org</p>\n\n<p>Vertretungsberechtigt: Eugen
            Rochko (Geschäftsführer)</p>\n\n<p>Umsatzsteuer Identifikationsnummer (USt-ID):
            DE344258260</p>\n\n<p>Handelsregister<br>\nGeführt bei: Amtsgericht Charlottenburg<br>\nNummer: HRB 230086
            B</p>\n'}

    Attributes:
        content (str): The rendered HTML content of the extended description.
        updated_at (datetime.datetime): A timestamp of when the extended description was last updated.
    """

    content: str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        updated_at = isoparse(d.pop("updated_at"))

        extended_description = cls(
            content=content,
            updated_at=updated_at,
        )

        extended_description.additional_properties = d
        return extended_description

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
