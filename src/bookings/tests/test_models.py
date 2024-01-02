from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.tests import create_test_user
from bookings.models import Booking
from bookings.validators import PAST_DATE_ERROR_MESSAGE, CHECK_OUT_DATE_ERROR_MESSAGE
from rooms.models import TYPE, Room
from rooms.tests.test_models import create_test_room
from utils.cases import ModelTestCase

User = get_user_model()


def create_test_booking(user=None, check_in=None, check_out=None, **extra_fields):
    if not user:
        user = create_test_user()

    if check_in is None:
        check_in = timezone.now() + timezone.timedelta(days=1)

    if check_out is None:
        check_out = timezone.now() + timezone.timedelta(days=11)

    return Booking.objects.create(user=user, check_in=check_in, check_out=check_out, **extra_fields)


class BookingModelTest(ModelTestCase):
    def setUp(self) -> None:
        self.Model = Booking

    def test_model_has_necessary_fields(self):
        necessary_fields = [
            'uuid',
            'user',
            'rooms',
            'type',
            'persons',
            'has_children',
            'is_paid',
            'check_in',
            'check_out',
            'updated',
            'created',
        ]
        self.assertModelHasNecessaryFields(self.Model, necessary_fields)

    def test_uuid_field_is_pk(self):
        field = self.get_field(self.Model, 'uuid')
        self.assertTrue(field.primary_key)

    def test_uuid_field_is_unique(self):
        field = self.get_field(self.Model, 'uuid')
        self.assertTrue(field.unique)

    def test_user_field_has_many_to_one_relation_with_user_model(self):
        field = self.get_field(self.Model, 'user')
        self.assertTrue(field.many_to_one)
        self.assertIs(field.related_model, User)

    def test_rooms_field_has_many_to_many_relation_with_room_model(self):
        field = self.get_field(self.Model, 'rooms')
        self.assertTrue(field.many_to_many)
        self.assertIs(field.related_model, Room)

    def test_type_field_is_standard_by_default(self):
        field = self.get_field(self.Model, 'type')
        self.assertEqual(field.default, TYPE.STANDARD)

    def test_persons_field_is_only_positive_int(self):
        field = self.get_field(self.Model, 'persons')
        self.assertIsInstance(field, models.PositiveSmallIntegerField)

    def test_persons_field_is_one_by_default(self):
        field = self.get_field(self.Model, 'persons')
        self.assertEqual(field.default, 1)

    def test_has_children_field_is_false_by_default(self):
        field = self.get_field(self.Model, 'has_children')
        self.assertFalse(field.default)

    def test_is_paid_field_is_false_by_default(self):
        field = self.get_field(self.Model, 'is_paid')
        self.assertFalse(field.default)

    def test_check_in_field_cannot_be_past_date(self):
        invalid_check_in = datetime.now() - timedelta(days=1)
        check_out = datetime.now() + timedelta(days=10)
        booking = create_test_booking(check_in=invalid_check_in.date(), check_out=check_out.date())

        with self.assertRaisesRegex(ValidationError, PAST_DATE_ERROR_MESSAGE):
            booking.full_clean()

    def test_check_out_field_cannot_be_past_date(self):
        check_in = datetime.now() + timedelta(days=1)
        invalid_check_out = datetime.now() - timedelta(days=10)
        booking = create_test_booking(check_in=check_in.date(), check_out=invalid_check_out.date())

        with self.assertRaisesRegex(ValidationError, PAST_DATE_ERROR_MESSAGE):
            booking.full_clean()

    def test_check_out_field_cannot_be_earlier_than_check_in_date(self):
        check_in = datetime.now() + timedelta(days=10)
        invalid_check_out = check_in - timedelta(days=1)
        booking = create_test_booking(check_in=check_in.date(), check_out=invalid_check_out.date())

        with self.assertRaisesRegex(ValidationError, CHECK_OUT_DATE_ERROR_MESSAGE):
            booking.full_clean()

    def test_model_instances_are_ordered_by_descending_created_date(self):
        attr = self.get_meta_attr(self.Model, 'ordering')
        self.assertIn('-created', attr)

    def test_get_str_rooms_method_returns_correct_value(self):
        room_1 = create_test_room(number='1')
        room_2 = create_test_room(number='2')
        bookings = create_test_booking()
        bookings.rooms.add(room_1)
        bookings.rooms.add(room_2)

        self.assertEqual(bookings.get_str_rooms(), '1, 2')

    def test_get_total_price_method_returns_correct_value(self):
        room_1 = create_test_room(number='1')
        room_2 = create_test_room(number='2')
        bookings = create_test_booking()
        bookings.rooms.add(room_1)
        bookings.rooms.add(room_2)

        expected_total_price = sum([room.room_data.price for room in bookings.rooms.all()])

        self.assertEqual(bookings.get_total_price(), expected_total_price)

    def test_get_str_type_method_returns_correct_type(self):
        booking = Booking(type=TYPE.LUXE)
        self.assertEqual(booking.get_str_type(), TYPE.choices[booking.type][1])
