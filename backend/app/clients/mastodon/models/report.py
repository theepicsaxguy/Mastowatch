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
    r"""Reports filed against users and/or statuses, to be taken action on by moderators.

    Example:
        {'id': '48914', 'action_taken': False, 'action_taken_at': None, 'category': 'spam', 'comment': 'Spam account',
            'forwarded': False, 'created_at': '2022-08-25T09:56:16.763Z', 'status_ids': ['108882889550545820'], 'rule_ids':
            None, 'target_account': {'id': '108366849347798387', 'username': 'Baluke', 'acct': 'Baluke', 'display_name':
            'Baluke Dental Studios', 'locked': False, 'bot': False, 'discoverable': False, 'group': False, 'created_at':
            '2022-05-26T00:00:00.000Z', 'note': '<p>Baluke Dental Studios is a full service dental lab offering fabrication,
            staining, and digital services. Advanced technologies and a meticulous process ensure reduced chair time, lower
            costs, and better patient outcomes with beautiful smiles. Talk to a representative today.</p><p><a
            href="https://baluke.com/" target="_blank" rel="nofollow noopener noreferrer"><span
            class="invisible">https://</span><span class="">baluke.com/</span><span class="invisible"></span></a></p>',
            'url': 'https://mastodon.social/@Baluke', 'avatar':
            'https://files.mastodon.social/accounts/avatars/108/366/849/347/798/387/original/dbcfe99ed5def0f4.png',
            'avatar_static':
            'https://files.mastodon.social/accounts/avatars/108/366/849/347/798/387/original/dbcfe99ed5def0f4.png',
            'header': 'https://static-cdn.mastodon.social/headers/original/missing.png', 'header_static': 'https://static-
            cdn.mastodon.social/headers/original/missing.png', 'followers_count': 0, 'following_count': 0, 'statuses_count':
            38, 'last_status_at': '2022-08-25', 'emojis': [], 'fields': []}}

    Attributes:
        action_taken (bool): Whether an action was taken yet.
        category (CategoryEnum):
        comment (str): The reason for the report.
        created_at (datetime.datetime): When the report was created.
        forwarded (bool): Whether the report was forwarded to a remote domain.
        id (str): The ID of the report in the database.
        target_account (Account): Represents a user of Mastodon and their associated profile. Example: {'id': '23634',
            'username': 'noiob', 'acct': 'noiob@awoo.space', 'display_name': 'ikea shark fan account', 'locked': False,
            'bot': False, 'created_at': '2017-02-08T02:00:53.274Z', 'note': '<p>:ms_rainbow_flag:\u200b
            :ms_bisexual_flagweb:\u200b :ms_nonbinary_flag:\u200b <a href="https://awoo.space/tags/awoo" class="mention
            hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>awoo</span}.space <a
            href="https://awoo.space/tags/admin" class="mention hashtag" rel="nofollow noopener noreferrer"
            target="_blank">#<span>admin</span} ~ <a href="https://awoo.space/tags/bi" class="mention hashtag" rel="nofollow
            noopener noreferrer" target="_blank">#<span>bi</span} ~ <a href="https://awoo.space/tags/nonbinary"
            class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>nonbinary</span} ~ compsci
            student ~ likes video <a href="https://awoo.space/tags/games" class="mention hashtag" rel="nofollow noopener
            noreferrer" target="_blank">#<span>games</span} and weird/ old electronics and will post obsessively about both
            ~ avatar by <span class="h-card"><a href="https://weirder.earth/@dzuk" class="u-url mention" rel="nofollow
            noopener noreferrer" target="_blank">@<span>dzuk</span}</span></p>', 'url': 'https://awoo.space/@noiob',
            'avatar': 'https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png',
            'avatar_static': 'https://files.mastodon.social/accounts/avatars/000/023/634/original/6ca8804dc46800ad.png',
            'header': 'https://files.mastodon.social/accounts/headers/000/023/634/original/256eb8d7ac40f49a.png',
            'header_static': 'https://files.mastodon.social/accounts/headers/000/023/634/original/256eb8d7ac40f49a.png',
            'followers_count': 547, 'following_count': 404, 'statuses_count': 28468, 'last_status_at': '2019-11-17',
            'emojis': [{'shortcode': 'ms_rainbow_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/028/691/original/6de008d6281f4f59.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/028/691/static/6de008d6281f4f59.png',
            'visible_in_picker': True}, {'shortcode': 'ms_bisexual_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/050/744/original/02f94a5fca7eaf78.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/050/744/static/02f94a5fca7eaf78.png',
            'visible_in_picker': True}, {'shortcode': 'ms_nonbinary_flag', 'url':
            'https://files.mastodon.social/custom_emojis/images/000/105/099/original/8106088bd4782072.png', 'static_url':
            'https://files.mastodon.social/custom_emojis/images/000/105/099/static/8106088bd4782072.png',
            'visible_in_picker': True}], 'fields': [{'name': 'Pronouns', 'value': 'they/them', 'verified_at': None},
            {'name': 'Alt', 'value': '<span class="h-card"><a href="https://cybre.space/@noiob" class="u-url mention"
            rel="nofollow noopener noreferrer" target="_blank">@<span>noiob</span}</span>', 'verified_at': None}, {'name':
            'Bots', 'value': '<span class="h-card"><a href="https://botsin.space/@darksouls" class="u-url mention"
            rel="nofollow noopener noreferrer" target="_blank">@<span>darksouls</span}</span>, <span class="h-card"><a
            href="https://botsin.space/@nierautomata" class="u-url mention" rel="nofollow noopener noreferrer"
            target="_blank">@<span>nierautomata</span}</span>, <span class="h-card"><a href="https://mastodon.social/@fedi"
            class="u-url mention" rel="nofollow noopener noreferrer" target="_blank">@<span>fedi</span}</span>, code for
            <span class="h-card"><a href="https://botsin.space/@awoobot" class="u-url mention" rel="nofollow noopener
            noreferrer" target="_blank">@<span>awoobot</span}</span>', 'verified_at': None}, {'name': 'Website', 'value':
            '<a href="http://shork.xyz" rel="nofollow noopener noreferrer" target="_blank"><span
            class="invisible">http://</span><span class="">shork.xyz</span><span class="invisible"></span}', 'verified_at':
            '2019-11-10T10:31:10.744+00:00'}]}.
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
