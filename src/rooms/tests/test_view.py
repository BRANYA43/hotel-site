from django.urls import reverse
from django.test import TestCase

from rooms.tests.test_models import create_test_room_data


class RoomDataListViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('rooms:room-list')

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'rooms/list.html')

    def test_view_contains_some_message_if_room_data_is_none(self):
        response = self.client.get(self.url)
        expected_text = "Rooms aren't added yet"

        self.assertContains(response, expected_text)

    def test_view_contains_some_info_if_room_data_is(self):
        room_data = create_test_room_data(single_beds=2, double_beds=1, description='some description')
        response = self.client.get(self.url)

        expected_text = [
            f'Title: {room_data.name}',
            f'Type: {room_data.type}',
            f'Persons: {room_data.persons}',
            f'Price: {room_data.price}.00 UAH',
            f'Description: {room_data.description}',
        ]

        for text in expected_text:
            self.assertContains(response, text)
