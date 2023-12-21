from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse, path

from accounts.urls import urlpatterns as acc_urls
from accounts.views import UserRegisterView
from core.urls import urlpatterns as core_urls
from utils.tests import test_view

User = get_user_model()


class UserRegisterViewTest(TestCase):
    def setUp(self) -> None:
        acc_urls.append(path('register/success/', test_view, name='user-register-success'))
        acc_urls.append(path('register/confirm-email/<uidb64>/<token>/', test_view, name='user-confirm-email'))
        core_urls.append(path('', test_view, name='home'))

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
