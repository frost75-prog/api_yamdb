from datetime import datetime as dt

from django.core.exceptions import ValidationError

from api_yamdb.settings import REGEX_SLUG


def validate_year(value):
    """
    Кастомный валидатор для поля year.
    Год выпуска не может быть больше текущего.
    """
    if value > dt.now().year:
        raise ValidationError(
            'Invalid year! Year must be less then current year.')
    elif value < 0:
        raise ValidationError(
            'Invalid year! Year must be biggest then zero.')
    return value


def validate_slug(value):
    """Кастомный валидатор для поля slug."""
    if not REGEX_SLUG.match(value):
        raise ValidationError(
            'Invalid slug! Change slug name')
    return value
