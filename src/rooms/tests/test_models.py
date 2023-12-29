from utils.cases import ModelTestCase
from rooms.models import Room, TYPE, STATUS


class RoomModelTest(ModelTestCase):
    def setUp(self) -> None:
        self.Model = Room

    def test_model_has_necessary_fields(self):
        necessary_fields = [
            'price',
            'type',
            'status',
            'single_beds',
            'double_beds',
        ]

        self.assertModelHasNecessaryFields(self.Model, necessary_fields)

    def test_type_is_standard_by_default(self):
        field = self.get_field(self.Model, 'type')
        self.assertEqual(field.default, TYPE.STANDARD)

    def test_status_is_free_by_default(self):
        field = self.get_field(self.Model, 'status')
        self.assertEqual(field.default, STATUS.FREE)

    def test_single_beds_is_zero_by_default(self):
        field = self.get_field(self.Model, 'single_beds')
        self.assertEqual(field.default, 0)

    def test_double_beds_is_zero_by_default(self):
        field = self.get_field(self.Model, 'double_beds')
        self.assertEqual(field.default, 0)

    def test_persons_get_quantity_by_beds(self):
        model = self.Model(single_beds=1, double_beds=1)
        self.assertEqual(model.persons, 3)
