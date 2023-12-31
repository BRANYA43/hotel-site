from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.tests import create_test_user
from bookings.models import Booking
from rooms.models import TYPE


class BookingCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = create_test_user(is_confirmed_email=True)
        self.client.force_login(self.user)
        self.url = reverse('bookings:booking-create')
        check_in = datetime.now() + timedelta(days=1)
        check_out = check_in + timedelta(days=10)
        self.data = {
            'user': self.user.id,
            'persons': 10,
            'type': TYPE.STANDARD,
            'is_children': False,
            'check_in': check_in.date(),
            'check_out': check_out.date(),
        }

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'bookings/create_form.html')

    def test_view_redirects_to_login_page_if_user_dont_login(self):
        self.client.logout()
        expected_url = reverse('accounts:user-login') + '?next=' + self.url
        response = self.client.get(self.url)

        self.assertRedirects(response, expected_url)

    def test_view_redirects_to_booking_list_page(self):
        response = self.client.post(self.url, self.data)

        self.assertRedirects(response, reverse('bookings:booking-list'))

    def test_view_create_booking_if_data_is_valid(self):
        self.client.post(self.url, self.data)

        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()

        self.assertEqual(booking.user.id, self.data['user'])
        self.assertEqual(booking.persons, self.data['persons'])
        self.assertEqual(booking.type, self.data['type'])
        self.assertFalse(booking.is_children)
        self.assertEqual(booking.check_in, self.data['check_in'])
        self.assertEqual(booking.check_out, self.data['check_out'])

    def test_view_dont_create_booking_if_data_is_invalid(self):
        del self.data['persons']
        self.client.post(self.url, self.data)

        self.assertEqual(Booking.objects.count(), 0)
