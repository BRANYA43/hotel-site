from datetime import timedelta, datetime


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
            'persons': 10,
            'type': TYPE.STANDARD,
            'has_children': False,
            'check_in': datetime.now() + timedelta(days=1),
            'check_out': datetime.now() + timedelta(days=10),
        }

    def test_form_has_only_this_fields(self):
        expected_fields = [
            'persons',
            'type',
            'has_children',
            'check_in',
            'check_out',
        ]

        fields = self.get_fields(self.Form, only_names=True, user=self.user)
        self.assertFieldListEqual(fields, expected_fields)

    def test_form_saves_if_data_is_valid(self):
        form = self.Form(data=self.data, instance=self.booking, user=self.user)
        form.is_valid()

        booking = form.save()  # not raise

        self.assertEqual(booking.type, self.data['type'])
        self.assertEqual(booking.persons, self.data['persons'])
        self.assertFalse(booking.has_children)
        self.assertEqual(booking.check_in, self.data['check_in'].date())
        self.assertEqual(booking.check_out, self.data['check_out'].date())

    def test_form_is_invalid_if_persons_is_zero(self):
        self.data['persons'] = 0
        form = self.Form(data=self.data, instance=self.booking, user=self.user)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, 'persons', NO_PERSONS_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_in_is_past_date(self):
        self.data['check_in'] -= timedelta(days=10)
        form = self.Form(data=self.data, instance=self.booking, user=self.user)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, PAST_DATE_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_out_is_past_date(self):
        self.data['check_out'] -= timedelta(days=20)
        form = self.Form(data=self.data, instance=self.booking, user=self.user)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, PAST_DATE_ERROR_MESSAGE)

    def test_form_is_invalid_if_check_out_is_earlier_than_check_in(self):
        self.data['check_in'] += timedelta(days=10)
        self.data['check_out'] = self.data['check_in'] - timedelta(days=1)
        form = self.Form(data=self.data, instance=self.booking, user=self.user)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, None, CHECK_OUT_DATE_ERROR_MESSAGE)

    def test_form_sets_user_before_saving_booking(self):
        form = self.Form(data=self.data, instance=self.booking, user=self.user)
        form.is_valid()
        booking = form.save()

        self.assertEqual(booking.user.pk, self.user.pk)
