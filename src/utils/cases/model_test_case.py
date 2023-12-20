from typing import Type

from django.db.models import Field, Model
from django.test import TestCase


class ModelTestCase(TestCase):
    @staticmethod
    def get_field(model: Type[Model], name: str) -> Type[Field]:
        return model._meta.get_field(name)

    @staticmethod
    def get_fields(model: Type[Model], *, only_names=False):
        fields = model._meta.get_fields()
        if only_names:
            return [field.name for field in fields]
        return fields

    @staticmethod
    def get_meta_attr(model: Type[Model], name: str):
        return getattr(model._meta, name)
