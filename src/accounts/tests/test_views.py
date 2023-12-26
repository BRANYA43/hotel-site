from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tests import create_test_user
from accounts.views import UserRegisterView

User = get_user_model()


class UserRegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:user-register')
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
            'confirmed_password': 'qwe123!@#',
        }

    def test_view_uses_correct_template_GET(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/register_form.html')

    def test_view_creates_user_POST(self):
        self.assertEqual(User.objects.count(), 0)

        self.client.post(self.url, self.data)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))

    def test_view_redirects_to_correct_page_POST(self):
        response = self.client.post(self.url, self.data)

        self.assertRedirects(response, reverse('accounts:user-register-success'))

    def test_view_send_mail_to_user_email_POST(self):
        self.client.post(self.url, self.data)

        self.assertIsNotNone(mail.outbox)

    def test_view_uses_necessary_templates_make_male(self):
        self.assertEqual(UserRegisterView.subject_template_name, 'accounts/subject_of_register_data_confirmation.html')
        self.assertEqual(UserRegisterView.body_template_name, 'accounts/body_of_register_data_confirmation.html')


class UserRegisterSuccessViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:user-register-success')

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/register_success.html')

    def test_view_contains_correct_text(self):
        expected_text = [
            'You registered the account success, now you need to confirm your email.',
            'We sent the email with the instructions to your email.',
            'Please, check your email and follow the instructions.',
        ]

        response = self.client.get(self.url)

        for text in expected_text:
            self.assertContains(response, text)


class UserConfirmEmailViewTest(TestCase):
    def setUp(self) -> None:
        self.user = create_test_user()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.name_view = 'accounts:user-confirm-email'
        self.url = reverse(self.name_view, args=[self.uidb64, self.token])

    def test_view_redirects_to_login_if_uidb_and_token_are_valid(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('accounts:user-login'))

    def test_view_redirects_to_failure_if_uidb_is_invalid(self):
        invalid_url = reverse(self.name_view, args=[b'invalid', self.token])
        response = self.client.get(invalid_url)

        self.assertRedirects(response, reverse('accounts:user-confirm-email-failure'))

    def test_view_redirects_to_failure_if_token_is_invalid(self):
        invalid_url = reverse(self.name_view, args=[self.uidb64, 'invalid'])
        response = self.client.get(invalid_url)

        self.assertRedirects(response, reverse('accounts:user-confirm-email-failure'))

    def test_view_set_is_confirmed_email_as_true_if_user_is_valid(self):
        self.client.get(self.url)
        self.user.refresh_from_db()

        self.assertTrue(self.user.is_confirmed_email)


class UserConfirmEmailFailureViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:user-confirm-email-failure')

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/confirm_email_failure.html')

    def test_view_contains_correct_text(self):
        expected_text = ['Failure try of confirming email. Please, try once yet.']
        response = self.client.get(self.url)

        for text in expected_text:
            self.assertContains(response, text)


class UserLoginViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:user-login')
        self.data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
        }
        self.user = create_test_user(**self.data)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'accounts/login_form.html')

    def test_view_does_not_login_user_if_credential_data_is_invalid(self):
        invalid_data = {'email': self.data['email'], 'password': 'wrong_password'}
        response = self.client.post(self.url, invalid_data)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        invalid_data = {'email': 'wrong_email@test.com', 'password': self.data['password']}
        response = self.client.post(self.url, invalid_data)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_view_does_not_login_user_if_user_did_not_confirm_email(self):
        response = self.client.post(self.url, self.data)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_view_logins_user(self):
        self.user.is_confirmed_email = True
        self.user.save()

        response = self.client.post(self.url, self.data)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_view_redirect_to_account(self):
        self.user.is_confirmed_email = True
        self.user.save()
        response = self.client.post(self.url, self.data)

        self.assertRedirects(response, reverse('accounts:user-account'))


class UserRegisterContinueViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:user-register-continue')
        self.user = create_test_user()
        self.profile = self.user.profile
        self.client.force_login(self.user)
        self.data = {
            'user': self.user.pk,
            'first_name': 'Rick',
            'last_name': 'Sanchez',
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
        }

    def test_view_redirects_to_login_page_if_user_is_not_logged(self):
        self.client.logout()
        expected_url = reverse('accounts:user-login') + '?next=' + reverse('accounts:user-register-continue')
        response = self.client.get(self.url)

        self.assertTrue(response.wsgi_request.user.is_anonymous)
        self.assertRedirects(response, expected_url)

    def test_view_redirects_to_account_page(self):
        response = self.client.post(self.url, self.data)

        self.assertRedirects(response, reverse('accounts:user-account'))

    def test_view_updates_user_profile(self):
        self.client.post(self.url, self.data)
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.first_name, self.data['first_name'])
        self.assertEqual(self.profile.last_name, self.data['last_name'])
        self.assertEqual(self.profile.birthday.strftime('%Y-%m-%d'), self.data['birthday'])
        self.assertEqual(self.profile.telephone, self.data['telephone'])

    def test_view_does_not_update_user_profile_if_data_is_invalid(self):
        invalid_data = {
            'first_name': 'Rick123',
            'last_name': 'Sanchez@!#',
            'birthday': '1958-07-03dasf',
            'telephone': '+38 (050)00 00',
        }
        self.client.post(self.url, invalid_data)
        self.profile.refresh_from_db()

        self.assertIsNone(self.profile.first_name)
        self.assertIsNone(self.profile.last_name)
        self.assertIsNone(self.profile.birthday)
        self.assertIsNone(self.profile.telephone)
