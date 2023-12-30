from utils.cases import ModelTestCase
from utils.models import DateMixin


class DateMixinTest(ModelTestCase):
    def setUp(self) -> None:
        self.Model = DateMixin

    def test_updated_is_set_after_each_save(self):
        field = self.get_field(self.Model, 'updated')
        self.assertTrue(field.auto_now)

    def test_created_is_set_for_first_save(self):
        field = self.get_field(self.Model, 'created')
        self.assertTrue(field.auto_now_add)
