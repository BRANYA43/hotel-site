from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.tests import create_test_user
from functional_tests.fucntional_test import FunctionalTest

User = get_user_model()


class AccountsAppTest(FunctionalTest):
    def setUp(self) -> None:
        super().setUp()
        self.user_data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
            'first_name': 'Rick',
            'last_name': 'Sanchez',
            'birthday': '07-03-1958',
            'telephone': '+380 000 00 00',
        }

    def test_user_pass_first_step_of_registration(self):
        url = self.live_server_url + reverse('user-register')
        self.browser.get(url)

        input_box = self.browser.find_element('id_email')
        input_box.send_keys(self.user_data['email'])

        input_box = self.browser.find_element('id_password')
        input_box.send_keys(self.user_data['password'])

        input_box = self.browser.find_element('id_confirmed_password')
        input_box.send_keys(self.user_data['password'])

        button = self.browser.find_element('id_sing_up')
        button.click()

        text = self.wait_for(
            lambda x: self.browser.find_element('id_success_message')  # not raise
        )
        expected_text = (
            'You finished first step of registration. We sent to you the instruction for confirmed your '
            'email. Check your email.'
        )
        self.assertEqual(text.text, expected_text)

    def test_user_pass_second_step_of_registration(self):
        user = create_test_user()
        user.is_confirmed_email = True

        url = self.live_server_url + reverse('user-register-continue', args=[user.id])
        self.browser.get(url)

        input_box = self.browser.find_element('id_first_name')
        input_box.send_keys(self.user_data['first_name'])

        input_box = self.browser.find_element('id_last_name')
        input_box.send_keys(self.user_data['last_name'])

        input_box = self.browser.find_element('id_birthday')
        input_box.send_keys(self.user_data['birthday'])

        input_box = self.browser.find_element('id_telephone')
        input_box.send_keys(self.user_data['telephone'])

        button = self.browser.find_element('id_finish')
        button.click()

        self.wait_for(
            lambda: self.browser.find_element('id_avatar')  # not raise
        )
