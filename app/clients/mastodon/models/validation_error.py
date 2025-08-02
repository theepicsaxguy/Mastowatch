from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.validation_error_details import ValidationErrorDetails


T = TypeVar("T", bound="ValidationError")


@_attrs_define
class ValidationError:
    """Represents a validation error with field-specific details.

    Attributes:
        error (str): The overall validation error message.
        details (ValidationErrorDetails): Detailed validation errors for each field.
    """

    error: str
    details: "ValidationErrorDetails"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.validation_error_details import ValidationErrorDetails

        d = src_dict.copy()
        error = d.pop("error")

        details = ValidationErrorDetails.from_dict(d.pop("details"))

        validation_error = cls(
            error=error,
            details=details,
        )

        validation_error.additional_properties = d
        return validation_error

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
