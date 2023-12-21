from accounts.forms import (
    EXISTED_USER_ERROR_MESSAGE,
    NOT_MATCH_PASSWORDS_ERROR_MESSAGE,
    SAVE_ERROR_MESSAGE,
    UserRegisterForm,
)
from accounts.tests import create_test_user
from utils.cases import FormTestCase


class UserRegisterFormTest(FormTestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
            'confirmed_password': 'qwe123!@#',
        }
        self.Form = UserRegisterForm

    def test_form_has_only_this_fields(self):
        expected_fields = [
            'email',
            'password',
            'confirmed_password',
        ]
        fields = self.get_fields(self.Form, only_names=True)
        self.assertFieldListEqual(fields, expected_fields)

    def test_form_create_user_with_correct_data(self):
        form = self.Form(data=self.data)
        self.assertTrue(form.is_valid())
        user = form.save()  # not raise

        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))

    def test_form_is_invalid_if_password_or_confirmed_password_is_empty(self):
        self.data['password'] = ''
        self.data['confirmed_password'] = ''
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertErrorDictHasError(form.errors, 'This field is required.')

    def test_form_is_invalid_if_password_and_confirmed_password_is_not_match(self):
        self.data['password'] = '!@#123qwe'
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertErrorDictHasError(form.errors, NOT_MATCH_PASSWORDS_ERROR_MESSAGE)

    def test_form_is_invalid_if_user_is_existed(self):
        create_test_user(self.data['email'], self.data['password'])
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertErrorDictHasError(form.errors, EXISTED_USER_ERROR_MESSAGE)

    def test_form_does_not_save_user_if_data_is_invalid(self):
        self.data['password'] = ''
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())

        with self.assertRaisesRegex(ValueError, SAVE_ERROR_MESSAGE):
            form.save()
