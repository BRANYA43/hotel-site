from typing import Type

from django.forms import Field, Form
from django.test import TestCase


class FormTestCase(TestCase):
    def get_field(self, form: Type[Form], name: str) -> Type[Field]:
        return form().fields[name]

    @staticmethod
    def get_fields(
        form: Type[Form],
        *,
        only_names=False,
        **params,
    ) -> list[Type[Field]] | list[str]:
        fields = form(**params).fields
        if only_names:
            return list(fields.keys())
        return list(fields.values())

    def assertFieldListEqual(self, fields: list[str], expected_fields: list[str]):
        fields.sort()
        expected_fields.sort()

        self.assertListEqual(fields, expected_fields)
