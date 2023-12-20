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
        field = self.get_field(TestModel, 'field_1')
        self.assertIsInstance(field, models.Field)

    def test_get_fields_returns_all_model_fields(self):
        fields = self.get_fields(TestModel)

        self.assertEqual(len(fields), 3)

        for field, field_class in zip(fields, (models.Field, models.TextField, models.IntegerField)):
            self.assertIsInstance(field, field_class)

    def test_get_fields_returns_names_of_all_model_fields(self):
        fields = self.get_fields(TestModel, only_names=True)

        self.assertEqual(len(fields), 3)

        for field, field_name in zip(fields, ('field_1', 'field_2', 'field_3')):
            self.assertEqual(field, field_name)

    def test_get_meta_attr_returns_correct_model_meta_attr(self):
        attr = self.get_meta_attr(TestModel, 'abstract')
        self.assertTrue(attr)

    def test_assertModelHasNecessaryFields_not_raise_error(self):
        necessary_fields = ['field_1', 'field_2']

        self.assertModelHasNecessaryFields(TestModel, necessary_fields)  # not raise

    def test_assertModelHasNecessaryFields_raise_error(self):
        necessary_fields = ['field_1', 'field_2', 'field_4']

        with self.assertRaisesRegex(AssertionError, r'Model does not has : "\w+"'):
            self.assertModelHasNecessaryFields(TestModel, necessary_fields)
