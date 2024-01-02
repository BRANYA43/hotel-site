from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from accounts.manager import UserManager
from accounts.models import Profile, User
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
            'email_is_confirmed',
            'joined',
            'last_login',
            'groups',
            'user_permissions',
        ]
        self.assertModelHasNecessaryFields(User, necessary_fields)

    def test_email_field_is_username_field(self):
        self.assertEqual(self.model.USERNAME_FIELD, 'email')

    def test_email_field_is_unique(self):
        field = self.get_field(User, 'email')
        self.assertTrue(field.unique)

    def test_password_field_max_length_is_20(self):
        field = self.get_field(User, 'password')
        self.assertEqual(field.max_length, 20)

    def test_is_active_field_is_true_by_default(self):
        field = self.get_field(User, 'is_active')
        self.assertTrue(field.default)

    def test_is_superuser_field_is_false_by_default(self):
        field = self.get_field(User, 'is_superuser')
        self.assertFalse(field.default)

    def test_is_staff_field_is_false_by_default(self):
        field = self.get_field(User, 'is_staff')
        self.assertFalse(field.default)

    def test_email_field_is_confirmed_is_false_by_default(self):
        field = self.get_field(User, 'email_is_confirmed')
        self.assertFalse(field.default)

    def test_joined_field_set_date_time_only_after_creating(self):
        field = self.get_field(User, 'joined')
        self.assertTrue(field.auto_now_add)

    def test_get_user_model_method_returns_this_model(self):
        self.assertIs(get_user_model(), self.model)

    def test_manager_is_UserManager(self):
        self.assertIsInstance(self.model.objects, UserManager)


class ProfileModelTest(ModelTestCase):
    model = Profile

    def test_model_has_necessary_fields(self):
        necessary_fields = [
            'user',
            'first_name',
            'last_name',
            'birthday',
            'telephone',
        ]
        self.assertModelHasNecessaryFields(Profile, necessary_fields)

    def test_model_has_one_to_one_relation_with_user_model(self):
        field = self.get_field(Profile, 'user')
        self.assertTrue(field.one_to_one)
        self.assertIs(field.related_model, get_user_model())

    def test_first_name_field_is_null(self):
        field = self.get_field(Profile, 'first_name')
        self.assertTrue(field.null)

    def test_last_name_field_is_null(self):
        field = self.get_field(Profile, 'last_name')
        self.assertTrue(field.null)

    def test_birthday_field_is_null(self):
        field = self.get_field(Profile, 'birthday')
        self.assertTrue(field.null)

    def test_telephone_field_is_null(self):
        field = self.get_field(Profile, 'telephone')
        self.assertTrue(field.null)

    def test_model_is_created_after_save_user_model(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()

        self.assertEqual(profile.user.id, user.id)

    def test_model_is_deleted_after_deleting_user_model(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        user.delete()

        self.assertEqual(Profile.objects.count(), 0)

    def test_has_necessary_data_property_returns_false_if_model_data_is_empty(self):
        profile = Profile()

        self.assertFalse(profile.has_necessary_data)

    def test_has_necessary_data_property_returns_false_if_any_model_field_is_none(self):
        data = {
            'last_name': 'Sanchez',
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
        }
        profile = Profile(**data)

        self.assertFalse(profile.has_necessary_data)

    def test_has_necessary_data_property_returns_true_if_model_data_is_full(self):
        data = {
            'first_name': 'Rick',
            'last_name': 'Sanchez',
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
        }
        profile = Profile(**data)

        self.assertTrue(profile.has_necessary_data)
