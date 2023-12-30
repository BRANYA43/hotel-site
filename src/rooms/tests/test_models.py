from django.db import models

from utils.cases import ModelTestCase

from rooms.models import RoomData, TYPE, Room, STATUS


def create_test_room_data(slug='slug', price='9999', **extra_field):
    return RoomData.objects.create(slug=slug, price=price, **extra_field)


def create_test_room(room_data=None, number=1, **extra_fields):
    if not room_data:
        room_data = create_test_room_data()
    return Room.objects.create(room_data=room_data, number=number, **extra_fields)


class RoomDataModelTest(ModelTestCase):
    def setUp(self) -> None:
        self.Model = RoomData

    def test_model_has_necessary_fields(self):
        necessary_fields = [
            'name' 'slug',
            'type',
            'single_beds',
            'double_beds',
            'price',
            'description',
            'updated',
            'created',
        ]
        self.assertModelHasNecessaryFields(self.Model, necessary_fields)

    def test_type_field_is_standard_by_default(self):
        field = self.get_field(self.Model, name='type')
        self.assertEqual(field.default, TYPE.STANDARD)

    def test_single_beds_field_can_be_null_by_default(self):
        field = self.get_field(self.Model, 'single_beds')
        self.assertTrue(field.null)

    def test_single_beds_field_is_only_positive_int(self):
        field = self.get_field(self.Model, 'single_beds')
        self.assertIsInstance(field, models.PositiveSmallIntegerField)

    def test_double_beds_field_can_be_null_by_default(self):
        field = self.get_field(self.Model, 'double_beds')
        self.assertTrue(field.null)

    def test_double_beds_field_is_only_positive_int(self):
        field = self.get_field(self.Model, 'double_beds')
        self.assertIsInstance(field, models.PositiveSmallIntegerField)

    def test_price_field_has_max_digits_as_ten(self):
        field = self.get_field(self.Model, 'price')
        self.assertEqual(field.max_digits, 10)

    def test_price_field_has_decimal_places_as_two(self):
        field = self.get_field(self.Model, 'price')
        self.assertEqual(field.decimal_places, 2)

    def test_description_field_can_be_null(self):
        field = self.get_field(self.Model, 'description')
        self.assertTrue(field.null)

    def test_description_field_can_be_blank(self):
        field = self.get_field(self.Model, 'description')
        self.assertTrue(field.blank)

    def test_model_instances_are_ordered_by_type(self):
        attr = self.get_meta_attr(self.Model, 'ordering')
        self.assertIn('type', attr)

    def test_persons_property_returns_quantity_by_beds(self):
        room_data = create_test_room_data(single_beds=1, double_beds=1)
        self.assertEqual(room_data.persons, 3)


class RoomModelTest(ModelTestCase):
    def setUp(self) -> None:
        self.Model = Room

    def test_model_has_necessary_fields(self):
        necessary_field = [
            'room_data',
            'number',
            'status',
            'is_available',
            'updated',
            'created',
        ]
        self.assertModelHasNecessaryFields(self.Model, necessary_field)

    def test_room_data_field_has_many_to_one_relations(self):
        field = self.get_field(self.Model, 'room_data')
        self.assertIsInstance(field, models.ForeignKey)

    def test_related_model_of_room_data_field_is_RoomData_model(self):
        field = self.get_field(self.Model, 'room_data')
        self.assertIs(field.related_model, RoomData)

    def test_number_field_is_unique(self):
        field = self.get_field(self.Model, 'number')
        self.assertTrue(field.unique)

    def test_status_field_is_free_by_default(self):
        field = self.get_field(self.Model, 'status')
        self.assertEqual(field.default, STATUS.FREE)

    def test_is_available_field_is_true_by_default(self):
        field = self.get_field(self.Model, 'is_available')
        self.assertTrue(field.default)

    def test_model_is_protect_to_delete(self):
        room = create_test_room()
        room_data = room.room_data

        with self.assertRaises(models.ProtectedError):
            room_data.delete()

    def test_model_instances_are_ordered_by_number(self):
        attr = self.get_meta_attr(self.Model, 'ordering')
        self.assertIn('number', attr)
