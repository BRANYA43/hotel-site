from django.test import TestCase

from accounts.manager import EMAIL_ERROR_MESSAGE, UserManager
from accounts.models import User


class UserManagerTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.manager = UserManager()
        self.manager.model = User

    def test_create_user_makes_correct_user_only_by_email_and_password(self):
        user = self.manager.create_user(**self.data)

        self.assertEqual(User.objects.count(), 1)
        self.assertIsNotNone(User.objects.get(id=user.id))

        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertFalse(user.is_confirmed_email)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_makes_correct_user(self):
        user = self.manager.create_superuser(**self.data)

        self.assertEqual(User.objects.count(), 1)
        self.assertIsNotNone(User.objects.get(id=user.id))

        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertTrue(user.is_confirmed_email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_raise_EmptyEmailError(self):
        self.data['email'] = ''
        with self.assertRaisesRegex(ValueError, EMAIL_ERROR_MESSAGE):
            self.manager.create_superuser(**self.data)

    def test_create_superuser_raise_EmptyEmailError(self):
        self.data['email'] = ''
        with self.assertRaisesRegex(ValueError, EMAIL_ERROR_MESSAGE):
            self.manager.create_superuser(**self.data)
