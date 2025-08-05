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
    from ..models.account import Account
    from ..models.rule import Rule
    from ..models.v1_instance_configuration import V1InstanceConfiguration
    from ..models.v1_instance_stats import V1InstanceStats
    from ..models.v1_instance_urls import V1InstanceUrls


T = TypeVar("T", bound="V1Instance")


@_attrs_define
class V1Instance:
    """Represents the software instance of Mastodon running on this domain.

    Example:
        {'uri': 'mastodon.social', 'title': 'Mastodon', 'short_description': 'The original server operated by the
            Mastodon gGmbH non-profit', 'description': '', 'email': 'staff@mastodon.social', 'version': '3.5.3', 'urls':
            {'streaming_api': 'wss://mastodon.social'}, 'stats': {'user_count': 812303, 'status_count': 38151616,
            'domain_count': 25255}, 'thumbnail':
            'https://files.mastodon.social/site_uploads/files/000/000/001/original/vlcsnap-2018-08-27-16h43m11s127.png',
            'languages': ['en'], 'registrations': False, 'approval_required': False, 'invites_enabled': True,
            'configuration': {'statuses': {'max_characters': 500, 'max_media_attachments': 4, 'characters_reserved_per_url':
            23}, 'media_attachments': {'supported_mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp',
            'video/webm', 'video/mp4', 'video/quicktime', 'video/ogg', 'audio/wave', 'audio/wav', 'audio/x-wav',
            'audio/x-pn-wave', 'audio/vnd.wave', 'audio/ogg', 'audio/vorbis', 'audio/mpeg', 'audio/mp3', 'audio/webm',
            'audio/flac', 'audio/aac', 'audio/m4a', 'audio/x-m4a', 'audio/mp4', 'audio/3gpp', 'video/x-ms-asf'],
            'image_size_limit': 10485760, 'image_matrix_limit': 16777216, 'video_size_limit': 41943040,
            'video_frame_rate_limit': 60, 'video_matrix_limit': 2304000}, 'polls': {'max_options': 4,
            'max_characters_per_option': 50, 'min_expiration': 300, 'max_expiration': 2629746}}, 'contact_account': {'id':
            '1', 'username': 'Gargron', 'acct': 'Gargron', 'display_name': 'Eugen', 'locked': False, 'bot': False,
            'discoverable': True, 'group': False, 'created_at': '2016-03-16T00:00:00.000Z', 'note': '<p>Founder, CEO and
            lead developer <span class="h-card"><a href="https://mastodon.social/@Mastodon" class="u-url
            mention">@<span>Mastodon</span></a></span>, Germany.</p>', 'url': 'https://mastodon.social/@Gargron', 'avatar':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/dc4286ceb8fab734.jpg', 'avatar_static':
            'https://files.mastodon.social/accounts/avatars/000/000/001/original/dc4286ceb8fab734.jpg', 'header':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/3b91c9965d00888b.jpeg', 'header_static':
            'https://files.mastodon.social/accounts/headers/000/000/001/original/3b91c9965d00888b.jpeg', 'followers_count':
            118944, 'following_count': 305, 'statuses_count': 72309, 'last_status_at': '2022-08-24', 'emojis': [], 'fields':
            [{'name': 'Patreon', 'value': '<a href="https://www.patreon.com/mastodon" target="_blank" rel="nofollow noopener
            noreferrer me"><span class="invisible">https://www.</span><span class="">patreon.com/mastodon</span><span
            class="invisible"></span></a>', 'verified_at': None}]}, 'rules': [{'id': '1', 'text': 'Sexually explicit or
            violent media must be marked as sensitive when posting'}, {'id': '2', 'text': 'No racism, sexism, homophobia,
            transphobia, xenophobia, or casteism'}, {'id': '3', 'text': 'No incitement of violence or promotion of violent
            ideologies'}, {'id': '4', 'text': 'No harassment, dogpiling or doxxing of other users'}, {'id': '5', 'text': 'No
            content illegal in Germany'}, {'id': '7', 'text': 'Do not share intentionally false or misleading
            information'}]}

    Attributes:
        approval_required (bool): Whether registrations require moderator approval.
        configuration (V1InstanceConfiguration): Configured values and limits for this website.
        description (str): An HTML-permitted description of the Mastodon site.
        email (str): An email that may be contacted for any inquiries.
        invites_enabled (bool): Whether invites are enabled.
        languages (list[str]): Primary languages of the website and its staff.
        registrations (bool): Whether registrations are enabled.
        rules (list['Rule']): An itemized list of rules for this website.
        short_description (str): A short, plain-text description defined by the admin.
        stats (V1InstanceStats): Statistics about how much information the instance contains.
        title (str): The title of the website.
        uri (str): The WebFinger domain name of the instance (not a URI/URL).
        urls (V1InstanceUrls): URLs of interest for clients apps.
        version (str): The version of Mastodon installed on the instance.
        contact_account (Union['Account', None, Unset]): A user that can be contacted, as an alternative to `email`.
        thumbnail (Union[None, Unset, str]): Banner image for the website.
    """

    approval_required: bool
    configuration: "V1InstanceConfiguration"
    description: str
    email: str
    invites_enabled: bool
    languages: list[str]
    registrations: bool
    rules: list["Rule"]
    short_description: str
    stats: "V1InstanceStats"
    title: str
    uri: str
    urls: "V1InstanceUrls"
    version: str
    contact_account: Union["Account", None, Unset] = UNSET
    thumbnail: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.account import Account

        approval_required = self.approval_required

        configuration = self.configuration.to_dict()

        description = self.description

        email = self.email

        invites_enabled = self.invites_enabled

        languages = self.languages

        registrations = self.registrations

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        short_description = self.short_description

        stats = self.stats.to_dict()

        title = self.title

        uri = self.uri

        urls = self.urls.to_dict()

        version = self.version

        contact_account: Union[None, Unset, dict[str, Any]]
        if isinstance(self.contact_account, Unset):
            contact_account = UNSET
        elif isinstance(self.contact_account, Account):
            contact_account = self.contact_account.to_dict()
        else:
            contact_account = self.contact_account

        thumbnail: Union[None, Unset, str]
        if isinstance(self.thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = self.thumbnail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "approval_required": approval_required,
                "configuration": configuration,
                "description": description,
                "email": email,
                "invites_enabled": invites_enabled,
                "languages": languages,
                "registrations": registrations,
                "rules": rules,
                "short_description": short_description,
                "stats": stats,
                "title": title,
                "uri": uri,
                "urls": urls,
                "version": version,
            }
        )
        if contact_account is not UNSET:
            field_dict["contact_account"] = contact_account
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account import Account
        from ..models.rule import Rule
        from ..models.v1_instance_configuration import V1InstanceConfiguration
        from ..models.v1_instance_stats import V1InstanceStats
        from ..models.v1_instance_urls import V1InstanceUrls

        d = dict(src_dict)
        approval_required = d.pop("approval_required")

        configuration = V1InstanceConfiguration.from_dict(d.pop("configuration"))

        description = d.pop("description")

        email = d.pop("email")

        invites_enabled = d.pop("invites_enabled")

        languages = cast(list[str], d.pop("languages"))

        registrations = d.pop("registrations")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = Rule.from_dict(rules_item_data)

            rules.append(rules_item)

        short_description = d.pop("short_description")

        stats = V1InstanceStats.from_dict(d.pop("stats"))

        title = d.pop("title")

        uri = d.pop("uri")

        urls = V1InstanceUrls.from_dict(d.pop("urls"))

        version = d.pop("version")

        def _parse_contact_account(data: object) -> Union["Account", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_account_type_0 = Account.from_dict(data)

                return contact_account_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Account", None, Unset], data)

        contact_account = _parse_contact_account(d.pop("contact_account", UNSET))

        def _parse_thumbnail(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail", UNSET))

        v1_instance = cls(
            approval_required=approval_required,
            configuration=configuration,
            description=description,
            email=email,
            invites_enabled=invites_enabled,
            languages=languages,
            registrations=registrations,
            rules=rules,
            short_description=short_description,
            stats=stats,
            title=title,
            uri=uri,
            urls=urls,
            version=version,
            contact_account=contact_account,
            thumbnail=thumbnail,
        )

        v1_instance.additional_properties = d
        return v1_instance

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
