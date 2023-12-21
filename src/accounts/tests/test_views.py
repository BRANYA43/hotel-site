from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, path

from accounts.urls import urlpatterns
from utils.tests import test_view

User = get_user_model()


class UserRegisterViewTest(TestCase):
    def setUp(self) -> None:
        urlpatterns.append(path('url/', test_view, name='user-register-first-success'))
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

        self.assertRedirects(response, reverse('accounts:user-register-first-success'))
