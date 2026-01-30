import phonenumbers
from typing import Optional


class PhoneValidationError(ValueError):
    """Custom phone validation error"""
    pass


def validate_phone_number(value: Optional[str]) -> Optional[str]:

    if value is None:
        return value

    try:
        parsed = phonenumbers.parse(value, None)

        if not phonenumbers.is_valid_number(parsed):
            raise PhoneValidationError("Invalid phone number")

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

    except phonenumbers.NumberParseException:
        raise PhoneValidationError("Invalid phone number format")