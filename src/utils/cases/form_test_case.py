from typing import Type

from django.forms import Field, Form
from django.forms.utils import ErrorDict
from django.test import TestCase


class FormTestCase(TestCase):
    def get_field(self, form: Type[Form], name: str) -> Type[Field]:
        return form().fields[name]

    @staticmethod
    def get_fields(form: Type[Form], *, only_names=False) -> list[Type[Field]] | list[str]:
        fields = form().fields
        if only_names:
            return list(fields.keys())
        return list(fields.values())

    def assertFieldListEqual(self, fields: list[str], expected_fields: list[str]):
        fields.sort()
        expected_fields.sort()

        self.assertListEqual(fields, expected_fields)

    def assertErrorDictHasError(self, error_dict: ErrorDict, message: str):
        messages = [msg for msgs in error_dict.values() for msg in msgs]
        self.assertIn(message, messages)
