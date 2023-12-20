from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from accounts.manager import UserManager
from accounts.models import User
from utils.cases import ModelTestCase


def create_test_user(email='rick.sanchez@test.com', password='qwe123!@#', **extra_field):
    return User.objects.create_user(email, password, **extra_field)


class UserModelTest(ModelTestCase):
    model = User

    def test_model_inherit_necessary_classes(self):
        self.assertTrue(issubclass(self.model, AbstractBaseUser))
        self.assertTrue(issubclass(self.model, PermissionsMixin))

    def test_model_has_necessary_fields(self):
        necessary_fields = [
            'email',
            'password',
            'is_active',
            'is_superuser',
            'is_staff',
            'is_confirmed_email',
            'joined',
            'last_login',
            'groups',
            'user_permissions',
        ]
        self.assertModelHasNecessaryFields(User, necessary_fields)

    def test_email_is_username_field(self):
        self.assertEqual(self.model.USERNAME_FIELD, 'email')

    def test_email_is_unique(self):
        field = self.get_field(User, 'email')
        self.assertTrue(field.unique)

    def test_password_max_length_is_20(self):
        field = self.get_field(User, 'password')
        self.assertEqual(field.max_length, 20)

    def test_is_active_is_true_by_default(self):
        field = self.get_field(User, 'is_active')
        self.assertTrue(field.default)

    def test_is_superuser_is_false_by_default(self):
        field = self.get_field(User, 'is_superuser')
        self.assertFalse(field.default)

    def test_is_staff_is_false_by_default(self):
        field = self.get_field(User, 'is_staff')
        self.assertFalse(field.default)

    def test_is_confirmed_email_is_false_by_default(self):
        field = self.get_field(User, 'is_confirmed_email')
        self.assertFalse(field.default)

    def test_joined_set_date_time_only_after_creating(self):
        field = self.get_field(User, 'joined')
        self.assertTrue(field.auto_now_add)

    def test_get_user_model_returns_this_model(self):
        self.assertIs(get_user_model(), self.model)

    def test_manager_is_UserManager(self):
        self.assertIsInstance(self.model.objects, UserManager)
