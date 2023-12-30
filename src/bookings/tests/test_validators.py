from datetime import timedelta, datetime
from unittest import TestCase

from django.core.exceptions import ValidationError

from bookings.validators import (
    validate_check_in_date,
    PAST_DATE_ERROR_MESSAGE,
    validate_check_out_date,
    CHECK_OUT_DATE_ERROR_MESSAGE,
)


class ValidateCheckInDateTest(TestCase):
    def test_validator_doesnt_raise_error(self):
        date = datetime.now() + timedelta(days=1)
        validate_check_in_date(date.date())  # not raise

    def test_validator_raises_error(self):
        date = datetime.now() - timedelta(days=1)
        self.assertRaisesRegex(ValidationError, PAST_DATE_ERROR_MESSAGE, validate_check_in_date, date.date())


class ValidateCheckOutDateTest(TestCase):
    def test_validator_doesnt_raise_error(self):
        check_in = datetime.now() + timedelta(days=1)
        date = check_in + timedelta(days=10)
        validate_check_out_date(date.date(), check_in.date())  # not raise

    def test_validator_raises_error(self):
        check_in = datetime.now() + timedelta(days=10)
        date = check_in - timedelta(days=1)
        self.assertRaisesRegex(
            ValidationError, CHECK_OUT_DATE_ERROR_MESSAGE, validate_check_out_date, date.date(), check_in.date()
        )

        date = date - timedelta(days=20)
        self.assertRaisesRegex(
            ValidationError, PAST_DATE_ERROR_MESSAGE, validate_check_out_date, date.date(), check_in.date()
        )
