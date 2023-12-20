from django.db import models

from utils.cases import ModelTestCase


class TestModel(models.Model):
    field_1 = models.Field()
    field_2 = models.TextField()
    field_3 = models.IntegerField()

    class Meta:
        abstract = True


class ModelTestCaseTest(ModelTestCase):
    model = TestModel

    def test_get_field_returns_correct_model_field(self):
        field = self.get_field('field_1')
        self.assertIsInstance(field, models.Field)

    def test_get_fields_returns_all_model_fields(self):
        fields = self.get_fields()

        self.assertEqual(len(fields), 3)

        for field, field_class in zip(fields, (models.Field, models.TextField, models.IntegerField)):
            self.assertIsInstance(field, field_class)

    def test_get_fields_returns_names_of_all_model_fields(self):
        fields = self.get_fields(only_names=True)

        self.assertEqual(len(fields), 3)

        for field, field_name in zip(fields, ('field_1', 'field_2', 'field_3')):
            self.assertEqual(field, field_name)

    def test_get_meta_attr_returns_correct_model_meta_attr(self):
        attr = self.get_meta_attr('abstract')
        self.assertTrue(attr)

    def test_assertFieldNamesEqual_raise_error(self):
        fields_1 = ['q', 'w', 'e']
        fields_2 = ['q', 'r', 'e']

        with self.assertRaisesRegex(AssertionError, 'Field names are not match'):
            self.assertFieldNamesEqual(fields_1, fields_2)

    def test_assertFieldNamesEqual_not_raise_error(self):
        fields_1 = ['q', 'w', 'e']
        fields_2 = ['q', 'w', 'e']

        self.assertFieldNamesEqual(fields_1, fields_2)  # not raise error
