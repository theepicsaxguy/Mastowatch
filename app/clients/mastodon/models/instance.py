from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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

    Example:
        {'domain': 'mastodon.social', 'title': 'Mastodon', 'version': '4.4.0-alpha.3', 'source_url':
            'https://github.com/mastodon/mastodon', 'description': 'The original server operated by the Mastodon gGmbH non-
            profit', 'usage': {'users': {'active_month': 123122}}, 'thumbnail': {'url':
            'https://files.mastodon.social/site_uploads/files/000/000/001/@1x/57c12f441d083cde.png', 'blurhash':
            'UeKUpFxuo~R%0nW;WCnhF6RjaJt757oJodS$', 'versions': {'@1x':
            'https://files.mastodon.social/site_uploads/files/000/000/001/@1x/57c12f441d083cde.png', '@2x':
            'https://files.mastodon.social/site_uploads/files/000/000/001/@2x/57c12f441d083cde.png'}}, 'icon': [{'src':
            'https://files.mastodon.social/site_uploads/files/000/000/003/36/accf17b0104f18e5.png', 'size': '36x36'},
            {'src': 'https://files.mastodon.social/site_uploads/files/000/000/003/72/accf17b0104f18e5.png', 'size':
            '72x72'}, {'src': 'https://files.mastodon.social/site_uploads/files/000/000/003/192/accf17b0104f18e5.png',
            'size': '192x192'}, {'src':
            'https://files.mastodon.social/site_uploads/files/000/000/003/512/accf17b0104f18e5.png', 'size': '512x512'}],
            'languages': ['en'], 'configuration': {'urls': {'streaming': 'wss://mastodon.social', 'about':
            'https://mastodon.social/about', 'privacy_policy': 'https://mastodon.social/privacy-policy', 'terms_of_service':
            'https://mastodon.social/terms-of-service'}, 'vapid': {'public_key':
            'BCkMmVdKDnKYwzVCDC99Iuc9GvId-x7-kKtuHnLgfF98ENiZp_aj-UNthbCdI70DqN1zUVis-x0Wrot2sBagkMc='}, 'accounts':
            {'max_featured_tags': 10, 'max_pinned_statuses': 4}, 'statuses': {'max_characters': 500,
            'max_media_attachments': 4, 'characters_reserved_per_url': 23}, 'media_attachments': {'supported_mime_types':
            ['image/jpeg', 'image/png', 'image/gif', 'image/heic', 'image/heif', 'image/webp', 'video/webm', 'video/mp4',
            'video/quicktime', 'video/ogg', 'audio/wave', 'audio/wav', 'audio/x-wav', 'audio/x-pn-wave', 'audio/vnd.wave',
            'audio/ogg', 'audio/vorbis', 'audio/mpeg', 'audio/mp3', 'audio/webm', 'audio/flac', 'audio/aac', 'audio/m4a',
            'audio/x-m4a', 'audio/mp4', 'audio/3gpp', 'video/x-ms-asf'], 'description_limit': 1500, 'image_size_limit':
            10485760, 'image_matrix_limit': 16777216, 'video_size_limit': 41943040, 'video_frame_rate_limit': 60,
            'video_matrix_limit': 2304000}, 'polls': {'max_options': 4, 'max_characters_per_option': 50, 'min_expiration':
            300, 'max_expiration': 2629746}, 'translation': {'enabled': True}}, 'registrations': {'enabled': False,
            'approval_required': False, 'reason_required': False, 'message': None, 'min_age': 16}, 'api_versions':
            {'mastodon': 1}, 'contact': {'email': 'staff@mastodon.social', 'account': {'id': '1', 'username': 'Gargron',
            'acct': 'Gargron', 'display_name': 'Eugen 💀', 'locked': False, 'bot': False, 'discoverable': True, 'group':
            False, 'created_at': '2016-03-16T00:00:00.000Z', 'note': '<p>Founder, CEO and lead developer <span
            class="h-card"><a href="https://mastodon.social/@Mastodon" class="u-url
            mention">@<span>Mastodon</span></a></span>, Germany.</p>', 'url': 'https://mastodon.social/@Gargron', 'avatar':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/dc4286ceb8fab734.jpg', 'avatar_static':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/dc4286ceb8fab734.jpg', 'header':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/3b91c9965d00888b.jpeg', 'header_static':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/3b91c9965d00888b.jpeg', 'followers_count':
            133026, 'following_count': 311, 'statuses_count': 72605, 'last_status_at': '2022-10-31', 'noindex': False,
            'emojis': [], 'fields': [{'name': 'Patreon', 'value': '<a href="https://www.patreon.com/mastodon"
            target="_blank" rel="nofollow noopener noreferrer me"><span class="invisible">https://www.</span><span
            class="">patreon.com/mastodon</span><span class="invisible"></span></a>', 'verified_at': None}]}}, 'rules':
            [{'id': '1', 'text': 'Sexually explicit or violent media must be marked as sensitive when posting'}, {'id': '2',
            'text': 'No racism, sexism, homophobia, transphobia, xenophobia, or casteism'}, {'id': '3', 'text': 'No
            incitement of violence or promotion of violent ideologies'}, {'id': '4', 'text': 'No harassment, dogpiling or
            doxxing of other users'}, {'id': '5', 'text': 'No content illegal in Germany'}, {'id': '7', 'text': 'Do not
            share intentionally false or misleading information'}]}

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
