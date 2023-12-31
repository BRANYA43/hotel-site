from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.tests import create_test_user
from bookings.models import Booking
from bookings.tests.test_models import create_test_booking
from rooms.models import TYPE
from rooms.tests.test_models import create_test_room


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


class BookingListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.client.force_login(self.user)
        self.url = reverse('bookings:booking-list')

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'bookings/list.html')

    def test_view_redirects_to_login_page_if_user_dont_login(self):
        self.client.logout()
        expected_url = reverse('accounts:user-login') + '?next=' + self.url
        response = self.client.get(self.url)

        self.assertRedirects(response, expected_url)

    def test_view_contains_some_message_if_booking_data_is_none(self):
        response = self.client.get(self.url)
        expected_text = "Bookings aren't made yet."

        self.assertContains(response, expected_text)

    def test_view_contains_some_info_if_booking_data_is(self):
        bookings = create_test_booking(self.user)
        response = self.client.get(self.url)

        expected_text = [
            f'UUID: {bookings.uuid}',
            "Rooms: Manager doesn't choose room/rooms for you.",
            f'Persons: {bookings.persons}',
            f'Type: {bookings.type}',
            'Total price: -',
            f'Check in date: {bookings.check_in.strftime("%d %b. %Y")}',
            f'Check out date: {bookings.check_out.strftime("%d %b. %Y")}',
            f'Created date: {bookings.created.strftime("%d %b. %Y, %I:%M %p")}',
        ]

        for text in expected_text:
            self.assertContains(response, text)

    def test_view_contains_some_info_if_booking_data_is_and_manager_chose_rooms(self):
        room_1 = create_test_room(number='1')
        room_2 = create_test_room(number='2')
        bookings = create_test_booking(self.user)
        bookings.rooms.add(room_1)
        bookings.rooms.add(room_2)
        response = self.client.get(self.url)

        expected_text = [
            f'UUID: {bookings.uuid}',
            f'Rooms: {bookings.get_str_rooms()}',
            f'Persons: {bookings.persons}',
            f'Type: {bookings.type}',
            f'Total price: {bookings.get_total_price()} UAH',
            f'Check in date: {bookings.check_in.strftime("%d %b. %Y")}',
            f'Check out date: {bookings.check_out.strftime("%d %b. %Y")}',
            f'Created date: {bookings.created.strftime("%d %b. %Y, %I:%M %p")}',
        ]

        for text in expected_text:
            self.assertContains(response, text)

    def test_view_contains_only_bookings_of_login_user(self):
        other_user = create_test_user('morty@test.com')
        other_bookings = create_test_booking(other_user)
        bookings = create_test_booking(self.user)

        unexpected_text = f'UUID: {other_bookings.uuid}'
        expected_text = f'UUID: {bookings.uuid}'

        response = self.client.get(self.url)

        self.assertNotContains(response, unexpected_text)
        self.assertContains(response, expected_text)

        self.client.logout()
        self.client.force_login(other_user)

        response = self.client.get(self.url)

        self.assertNotContains(response, expected_text)
        self.assertContains(response, unexpected_text)
