import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PrivacyPolicy")


@_attrs_define
class PrivacyPolicy:
    r"""Represents the privacy policy of the instance.

    Example:
        {'updated_at': '2022-10-07T00:00:00+00:00', 'content': '<p>This privacy policy describes how example.com
            (&quot;example.com&quot;, &quot;we&quot;, &quot;us&quot;) collects,\nprotects and uses the personally
            identifiable information you may provide\nthrough the example.com website or its API.</p>\n\n<h1>What
            information do we collect?</h1>\n\n<ul>\n<li><strong>Basic account information</strong>: If you register on this
            server, you may be\nasked to enter a username, an e-mail address and a password.</li>\n<li><strong>Posts,
            following and other public information</strong>: The list of people you\nfollow is listed publicly, the same is
            true for your followers.</li>\n<li><strong>Direct and followers-only posts</strong>: All posts are stored and
            processed on the\nserver. You may\ntoggle an option to approve and reject new followers manually in the
            settings.\n<strong>Please keep in mind that the operators of the server and any receiving\nserver may view such
            messages</strong>, and that recipients may screenshot, copy or\notherwise re-share them. <strong>Do not share
            any sensitive information over\nMastodon.</strong></li>\n<li><strong>IPs and other metadata</strong>: When you
            log in, we record the IP address you log\nin from, as well as the name of your browser
            application.</li>\n</ul>\n\n<hr>\n\n<p>This document is CC-BY-SA. Originally adapted from the <a
            href="https://github.com/discourse/discourse">Discourse privacy\npolicy</a>.</p>\n'}

    Attributes:
        content (str): The rendered HTML content of the privacy policy.
        updated_at (datetime.datetime): A timestamp of when the privacy policy was last updated.

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

        privacy_policy = cls(
            content=content,
            updated_at=updated_at,
        )

        privacy_policy.additional_properties = d
        return privacy_policy

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
