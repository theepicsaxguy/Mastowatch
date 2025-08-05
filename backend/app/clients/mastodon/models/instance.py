from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_api_versions import InstanceApiVersions
    from ..models.instance_configuration import InstanceConfiguration
    from ..models.instance_contact import InstanceContact
    from ..models.instance_icon import InstanceIcon
    from ..models.instance_registrations import InstanceRegistrations
    from ..models.instance_thumbnail import InstanceThumbnail
    from ..models.instance_usage import InstanceUsage
    from ..models.rule import Rule


T = TypeVar("T", bound="Instance")


@_attrs_define
class Instance:
    """Represents the software instance of Mastodon running on this domain.

    Attributes:
        api_versions (InstanceApiVersions): Information about which version of the API is implemented by this server. It
            contains at least a `mastodon` attribute, and other implementations may have their own additional attributes.
        configuration (InstanceConfiguration): Configured values and limits for this website.
        contact (InstanceContact): Hints related to contacting a representative of the website.
        description (str): A short, plain-text description defined by the admin.
        domain (str): The WebFinger domain name of the instance.
        icon (list['InstanceIcon']): The list of available size variants for this instance configured icon.
        languages (list[str]): Primary languages of the website and its staff.
        registrations (InstanceRegistrations): Information about registering for this website.
        rules (list['Rule']): An itemized list of rules for this website.
        source_url (str): The URL for the source code of the software running on this instance, in keeping with AGPL
            license requirements.
        thumbnail (InstanceThumbnail): An image used to represent this instance.
        title (str): The title of the website.
        usage (InstanceUsage): Usage data for this instance.
        version (str): The version of Mastodon installed on the instance.
    """

    api_versions: "InstanceApiVersions"
    configuration: "InstanceConfiguration"
    contact: "InstanceContact"
    description: str
    domain: str
    icon: list["InstanceIcon"]
    languages: list[str]
    registrations: "InstanceRegistrations"
    rules: list["Rule"]
    source_url: str
    thumbnail: "InstanceThumbnail"
    title: str
    usage: "InstanceUsage"
    version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_versions = self.api_versions.to_dict()

        configuration = self.configuration.to_dict()

        contact = self.contact.to_dict()

        description = self.description

        domain = self.domain

        icon = []
        for icon_item_data in self.icon:
            icon_item = icon_item_data.to_dict()
            icon.append(icon_item)

        languages = self.languages

        registrations = self.registrations.to_dict()

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        source_url = self.source_url

        thumbnail = self.thumbnail.to_dict()

        title = self.title

        usage = self.usage.to_dict()

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_versions": api_versions,
                "configuration": configuration,
                "contact": contact,
                "description": description,
                "domain": domain,
                "icon": icon,
                "languages": languages,
                "registrations": registrations,
                "rules": rules,
                "source_url": source_url,
                "thumbnail": thumbnail,
                "title": title,
                "usage": usage,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_api_versions import InstanceApiVersions
        from ..models.instance_configuration import InstanceConfiguration
        from ..models.instance_contact import InstanceContact
        from ..models.instance_icon import InstanceIcon
        from ..models.instance_registrations import InstanceRegistrations
        from ..models.instance_thumbnail import InstanceThumbnail
        from ..models.instance_usage import InstanceUsage
        from ..models.rule import Rule

        d = dict(src_dict)
        api_versions = InstanceApiVersions.from_dict(d.pop("api_versions"))

        configuration = InstanceConfiguration.from_dict(d.pop("configuration"))

        contact = InstanceContact.from_dict(d.pop("contact"))

        description = d.pop("description")

        domain = d.pop("domain")

        icon = []
        _icon = d.pop("icon")
        for icon_item_data in _icon:
            icon_item = InstanceIcon.from_dict(icon_item_data)

            icon.append(icon_item)

        languages = cast(list[str], d.pop("languages"))

        registrations = InstanceRegistrations.from_dict(d.pop("registrations"))

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = Rule.from_dict(rules_item_data)

            rules.append(rules_item)

        source_url = d.pop("source_url")

        thumbnail = InstanceThumbnail.from_dict(d.pop("thumbnail"))

        title = d.pop("title")

        usage = InstanceUsage.from_dict(d.pop("usage"))

        version = d.pop("version")

        instance = cls(
            api_versions=api_versions,
            configuration=configuration,
            contact=contact,
            description=description,
            domain=domain,
            icon=icon,
            languages=languages,
            registrations=registrations,
            rules=rules,
            source_url=source_url,
            thumbnail=thumbnail,
            title=title,
            usage=usage,
            version=version,
        )

        instance.additional_properties = d
        return instance

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
