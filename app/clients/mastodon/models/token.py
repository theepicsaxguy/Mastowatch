from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Token")


@_attrs_define
class Token:
    """Represents an OAuth token used for authenticating with the API and performing actions.

    Example:
        {'access_token': 'ZA-Yj3aBD8U8Cm7lKUp-lm9O9BmDgdhHzDeqsY8tlL0', 'token_type': 'Bearer', 'scope': 'read write
            follow push', 'created_at': 1573979017}

    Attributes:
        access_token (str): An OAuth token to be used for authorization.
        created_at (float): When the token was generated.
        scope (str): The OAuth scopes granted by this token, space-separated.
        token_type (str): The OAuth token type. Mastodon uses `Bearer` tokens.

    """

    access_token: str
    created_at: float
    scope: str
    token_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        created_at = self.created_at

        scope = self.scope

        token_type = self.token_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
                "created_at": created_at,
                "scope": scope,
                "token_type": token_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_token = d.pop("access_token")

        created_at = d.pop("created_at")

        scope = d.pop("scope")

        token_type = d.pop("token_type")

        token = cls(
            access_token=access_token,
            created_at=created_at,
            scope=scope,
            token_type=token_type,
        )

        token.additional_properties = d
        return token

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
