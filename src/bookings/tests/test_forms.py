from datetime import timedelta, datetime

from django import forms

from accounts.tests import create_test_user
from bookings.forms import BookingCreateForm, NO_PERSONS_ERROR_MESSAGE
from bookings.models import Booking
from bookings.validators import PAST_DATE_ERROR_MESSAGE, CHECK_OUT_DATE_ERROR_MESSAGE
from rooms.models import TYPE
from utils.cases import FormTestCase


class BookingCreateFormTest(FormTestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.booking = Booking()
        self.Form = BookingCreateForm
        self.data = {
            'user': self.user.id,
            'persons': 10,
            'type': TYPE.STANDARD,
            'is_children': False,
            'check_in': datetime.now() + timedelta(days=1),
            'check_out': datetime.now() + timedelta(days=10),
        }

    def test_form_has_only_this_fields(self):
        expected_fields = [
            'user',
            'persons',
            'type',
            'is_children',
            'check_in',
            'check_out',
        ]

        fields = self.get_fields(self.Form, only_names=True)
        self.assertFieldListEqual(fields, expected_fields)

    def test_form_saves_if_data_is_valid(self):
        form = self.Form(data=self.data, instance=self.booking)
        form.is_valid()

        booking = form.save()  # not raise

        self.assertEqual(booking.user.id, self.data['user'])
        self.assertEqual(booking.type, self.data['type'])
        self.assertEqual(booking.persons, self.data['persons'])
        self.assertFalse(booking.is_children)
        self.assertEqual(booking.check_in, self.data['check_in'].date())
        self.assertEqual(booking.check_out, self.data['check_out'].date())

    def test_form_is_invalid_if_persons_is_zero(self):
        self.data['persons'] = 0
        form = self.Form(data=self.data, instance=self.booking)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, 'persons', NO_PERSONS_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_in_is_past_date(self):
        self.data['check_in'] -= timedelta(days=10)
        form = self.Form(data=self.data, instance=self.booking)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, PAST_DATE_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_out_is_past_date(self):
        self.data['check_out'] -= timedelta(days=20)
        form = self.Form(data=self.data, instance=self.booking)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, PAST_DATE_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_out_is_earlier_than_check_in(self):
        self.data['check_in'] += timedelta(days=10)
        self.data['check_out'] = self.data['check_in'] - timedelta(days=1)
        form = self.Form(data=self.data, instance=self.booking)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, CHECK_OUT_DATE_ERROR_MESSAGE)

    def test_user_field_is_hidden(self):
        field = self.get_field(self.Form, 'user')
        self.assertIs(field.hidden_widget, forms.HiddenInput)
