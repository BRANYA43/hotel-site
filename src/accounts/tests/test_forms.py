from django.forms import DateInput
from django.http import HttpRequest

from accounts import forms
from accounts.tests import create_test_user
from utils.cases import FormTestCase


class UserRegisterFormTest(FormTestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
            'confirmed_password': 'qwe123!@#',
        }
        self.Form = forms.UserRegisterForm

    def test_form_has_only_this_fields(self):
        expected_fields = [
            'email',
            'password',
            'confirmed_password',
        ]
        fields = self.get_fields(self.Form, only_names=True)
        self.assertFieldListEqual(fields, expected_fields)

    def test_form_creates_user_with_correct_data(self):
        form = self.Form(data=self.data)
        self.assertTrue(form.is_valid())
        user = form.save()  # not raise

        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))

    def test_form_is_invalid_if_password_or_confirmed_password_are_empty(self):
        self.data['password'] = ''
        self.data['confirmed_password'] = ''
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'confirmed_password', 'This field is required.')

    def test_form_is_invalid_if_password_and_confirmed_password_are_not_match(self):
        self.data['password'] = '!@#123qwe'
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'confirmed_password', forms.NOT_MATCH_PASSWORDS_ERROR_MESSAGE)

    def test_form_is_invalid_if_user_is_existed(self):
        create_test_user(self.data['email'], self.data['password'])
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'email', forms.EXISTED_USER_ERROR_MESSAGE)

    def test_form_doesnt_save_user_if_data_is_invalid(self):
        self.data['password'] = ''
        form = self.Form(data=self.data)

        self.assertFalse(form.is_valid())

        with self.assertRaisesRegex(ValueError, forms.SAVE_ERROR_MESSAGE):
            form.save()


class UserLoginFormTest(FormTestCase):
    def setUp(self) -> None:
        self.Form = forms.UserLoginForm
        self.data = {
            'email': 'rich.sanchez@gmail.com',
            'password': 'qwe123!@#',
        }
        self.request = HttpRequest()

    def test_form_has_this_fields(self):
        expected_fields = ['email', 'password']
        fields = self.get_fields(self.Form, only_names=True, request=self.request)

        self.assertFieldListEqual(fields, expected_fields)

    def test_form_is_invalid_if_credential_data_is_invalid(self):
        form = self.Form(self.request, data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, None, forms.INVALID_CREDENTIAL_DATA_ERROR_MESSAGE)

    def test_form_is_invalid_if_user_did_not_confirm_email(self):
        create_test_user(**self.data)
        form = self.Form(self.request, data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, None, forms.NOT_CONFIRMED_EMAIL_ERROR_MESSAGE)

    def test_form_gets_user_as_none_if_credential_data_is_invalid(self):
        form = self.Form(self.request, data=self.data)
        form.is_valid()

        self.assertIsNone(form.get_user())

    def test_form_gets_user_if_credential_data_is_valid(self):
        user = create_test_user(**self.data)
        form = self.Form(self.request, data=self.data)
        form.is_valid()

        form_user = form.get_user()

        self.assertIsNotNone(form_user)
        self.assertEqual(form_user.id, user.id)


class ProfileUpdateFormMixinTest(FormTestCase):
    def setUp(self) -> None:
        user = create_test_user()
        self.profile = user.profile
        self.Form = forms.ProfileUpdateFormMixin
        self.data = {
            'first_name': 'Rick',
            'last_name': 'Sanchez',
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
        }

    def test_form_updates_user_profile(self):
        form = self.Form(instance=self.profile, data=self.data)

        self.assertTrue(form.is_valid())

        profile = form.save()

        self.assertEqual(profile.first_name, self.data['first_name'])
        self.assertEqual(profile.last_name, self.data['last_name'])
        self.assertEqual(profile.birthday.strftime('%Y-%m-%d'), self.data['birthday'])
        self.assertEqual(profile.telephone, self.data['telephone'])

    def test_form_doesnt_update_user_profile_if_data_is_invalid(self):
        self.data = {}
        form = self.Form(instance=self.profile, data=self.data)

        self.assertFalse(form.is_valid())

        self.assertFormError(form, 'first_name', 'This field is required.')
        self.assertFormError(form, 'last_name', 'This field is required.')
        self.assertFormError(form, 'birthday', 'This field is required.')
        self.assertFormError(form, 'telephone', 'This field is required.')

    @staticmethod
    def get_cyrillic_and_latin_alfabet():
        latin = ''.join(chr(code) for code in range(ord('a'), ord('z') + 1))
        cyrillic = ''.join(chr(code) for code in range(ord('а'), ord('я') + 1))
        cyrillic += 'іїєґ'

        return latin + latin.upper() + cyrillic + cyrillic.upper()

    def test_form_is_valid_if_first_and_last_names_contain_only_letters_of_cyrillic_or_latin(self):
        self.data['first_name'] = self.get_cyrillic_and_latin_alfabet()
        self.data['last_name'] = self.get_cyrillic_and_latin_alfabet()

        form = self.Form(instance=self.profile, data=self.data)

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_if_first_and_last_names_contain_not_only_letters(self):
        self.data['first_name'] += '123!#$'
        self.data['last_name'] += '123!#$'

        form = self.Form(instance=self.profile, data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'first_name', forms.INVALID_NAME_ERROR_MESSAGE.format('first'))
        self.assertFormError(form, 'last_name', forms.INVALID_NAME_ERROR_MESSAGE.format('last'))

    def test_form_is_invalid_if_telephone_is_less_ten_numbers(self):
        self.data['telephone'] = '+38 000 00 00'

        form = self.Form(instance=self.profile, data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'telephone', forms.INVALID_TELEPHONE_ERROR_MESSAGE)

    def test_form_is_invalid_if_telephone_is_more_twelve_numbers(self):
        self.data['telephone'] += '0'

        form = self.Form(instance=self.profile, data=self.data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'telephone', forms.INVALID_TELEPHONE_ERROR_MESSAGE)

    def test_birthday_field_has_date_input_widget(self):
        field = self.get_field(self.Form, 'birthday')
        self.assertIsInstance(field.widget, DateInput)


class UserRegisterContinueFormTest(FormTestCase):
    def test_form_inherits_ProfileUpdateFormMixin(self):
        self.assertTrue(issubclass(forms.UserRegisterContinueForm, forms.ProfileUpdateFormMixin))


class UserAccountFormTest(FormTestCase):
    def test_form_inherits_ProfileUpdateFormMixin(self):
        self.assertTrue(issubclass(forms.UserAccountForm, forms.ProfileUpdateFormMixin))
