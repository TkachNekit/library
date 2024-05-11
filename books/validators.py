from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_not_future_date(value):
    """
    Validator function to ensure that the provided date is not in the future.
    """
    if value > timezone.now().date():
        raise ValidationError("Publication date cannot be in the future.")
