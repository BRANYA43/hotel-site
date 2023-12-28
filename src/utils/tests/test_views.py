from django.test import TestCase

from django.http import HttpResponse
from django.urls import reverse


def imitating_view(request):
    return HttpResponse(request)


class HomeViewTest(TestCase):
    def test_view_uses_correct_template(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'home.html')
