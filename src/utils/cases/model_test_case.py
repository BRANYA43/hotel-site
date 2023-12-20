from typing import Type

from django.db.models import Field, Model
from django.test import TestCase


class ModelTestCase(TestCase):
    model: Type[Model]

    def get_field(self, name: str) -> Type[Field]:
        return self.model._meta.get_field(name)

    def get_fields(self, *, only_names=False):
        fields = self.model._meta.get_fields()
        if only_names:
            return [field.name for field in fields]
        return fields

    def get_meta_attr(self, name: str):
        return getattr(self.model._meta, name)

    def assertFieldNamesEqual(self, fields: list[str], expected_fields: list[str], msg='Field names are not match'):
        fields.sort()
        expected_fields.sort()

        self.assertListEqual(fields, expected_fields, msg)
