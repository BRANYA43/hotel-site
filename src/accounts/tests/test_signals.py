from django.test import TestCase

from accounts.models import Profile
from accounts.tests import create_test_user


class CreateProfileSignalTest(TestCase):
    def test_signal_creates_profile_after_save_user_model(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.first()

        self.assertEqual(profile.user.id, user.id)

    def test_signal_creates_profile_if_user_model_doesnt_have_it(self):
        user = create_test_user()

        self.assertEqual(Profile.objects.count(), 1)

        user.save()

        self.assertEqual(Profile.objects.count(), 1)
