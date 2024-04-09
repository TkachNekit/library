from django.core.exceptions import ValidationError
import re


def validate_phone_number(value):
    """
    Validate that the input is a valid phone number.
    """
    # Define a regular expression pattern for a valid phone number
    phone_number_pattern = r'^\+?1?\d{9,15}$'

    # Compile the regular expression pattern
    phone_number_regex = re.compile(phone_number_pattern)

    # Check if the value matches the regular expression pattern
    if not phone_number_regex.match(value):
        raise ValidationError('Invalid phone number format.')
