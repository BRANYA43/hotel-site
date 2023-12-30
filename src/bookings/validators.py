from datetime import datetime

from django.core.exceptions import ValidationError

PAST_DATE_ERROR_MESSAGE = 'Date cannot be past.'
CHECK_OUT_DATE_ERROR_MESSAGE = 'Check out date cannot be earlier than check in date.'


def validate_check_in_date(value):
    if value < datetime.now().date():
        raise ValidationError(PAST_DATE_ERROR_MESSAGE, code='invalid_date')


def validate_check_out_date(value, check_in):
    if value < datetime.now().date():
        raise ValidationError(PAST_DATE_ERROR_MESSAGE, code='invalid_date')

    if value < check_in:
        raise ValidationError(CHECK_OUT_DATE_ERROR_MESSAGE, code='invalid_date')
