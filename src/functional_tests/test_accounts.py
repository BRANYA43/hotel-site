import re

from django.contrib.auth import get_user_model
from django.core import mail

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
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
        }

    def test_user_registers_on_site(self):
        # User goes to site to start registration
        self.browser.get(self.live_server_url)

        # User finds a registering link in a navbar and clicks on it
        self.browser.find_element(value='id_navbar').find_element(value='id_registering_link').click()

        # User inputs his credentials data and clicks on sing up
        self.wait_for(lambda: self.browser.find_element(value='id_register_form'))

        self.enter_to_input_field(self.user_data['email'], value='id_email')
        self.enter_to_input_field(self.user_data['password'], value='id_password')
        self.enter_to_input_field(self.user_data['password'], value='id_confirmed_password')

        self.browser.find_element(value='id_registering_button').click()

        # User follows to a page with a message of registering success. User follows instruction from the message.
        # User checks his email and clicks on the link for confirming email.
        self.wait_for(lambda: self.browser.find_element(value='id_success_message'))

        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        url = re.search(r'(http|https)://[^/]+/account/confirm-email/[^/]+/[^/]+/', body).group()
        self.browser.get(url)

        # User follows to a page with a message of confirming email success. User follows instruction from the message
        # and click on sing in.
        self.wait_for(lambda: self.browser.find_element(value='id_success_message'))

        self.browser.find_element(value='id_login_message_link').click()

        # User inputs his credential data and click on sing in
        self.wait_for(lambda: self.browser.find_element(value='id_login_form'))

        self.enter_to_input_field(self.user_data['email'], value='id_email')
        self.enter_to_input_field(self.user_data['password'], value='id_password')

        self.browser.find_element(value='id_login_button').click()

        # This is first login for User, so he must enter additional data to finish registration and clicks on finishing
        # button
        self.wait_for(lambda: self.browser.find_element(value='id_register_continue_form'))

        self.enter_to_input_field(self.user_data['first_name'], value='id_first_name')
        self.enter_to_input_field(self.user_data['last_name'], value='id_last_name')
        self.enter_to_input_field(self.user_data['birthday'], value='id_birthday')
        self.enter_to_input_field(self.user_data['telephone'], value='id_telephone')

        self.browser.find_element(value='id_finishing_button').click()

        # User follows to his account and checks his input data
        self.wait_for(lambda: self.browser.find_element(value='id_account_form'))

        first_name = self.browser.find_element(value='id_first_name').get_attribute('value')
        last_name = self.browser.find_element(value='id_last_name').get_attribute('value')
        birthday = self.browser.find_element(value='id_birthday').get_attribute('value')
        telephone = self.browser.find_element(value='id_telephone').get_attribute('value')

        self.assertEqual(first_name, self.user_data['first_name'])
        self.assertEqual(last_name, self.user_data['last_name'])
        self.assertEqual(birthday, self.user_data['birthday'])
        self.assertEqual(telephone, self.user_data['telephone'])

    def test_user_can_login_and_logout(self):
        user = create_test_user()
        user.email_is_confirmed = True
        user.save()
        profile = user.profile
        profile.first_name = self.user_data['first_name']
        profile.last_name = self.user_data['last_name']
        profile.birthday = self.user_data['birthday']
        profile.telephone = self.user_data['telephone']
        profile.save()

        # User goes to site to start registration
        self.browser.get(self.live_server_url)

        # User finds a login link in a navbar and clicks on it
        self.browser.find_element(value='id_navbar').find_element(value='id_login_link').click()

        # User inputs his credential data and click on sing in
        self.wait_for(lambda: self.browser.find_element(value='id_login_form'))

        self.enter_to_input_field(self.user_data['email'], value='id_email')
        self.enter_to_input_field(self.user_data['password'], value='id_password')

        self.browser.find_element(value='id_login_button').click()

        # User follows to account page and see his account data
        self.wait_for(lambda: self.browser.find_element(value='id_account_form'))

        first_name = self.browser.find_element(value='id_first_name').get_attribute('value')
        last_name = self.browser.find_element(value='id_last_name').get_attribute('value')
        birthday = self.browser.find_element(value='id_birthday').get_attribute('value')
        telephone = self.browser.find_element(value='id_telephone').get_attribute('value')

        self.assertEqual(first_name, self.user_data['first_name'])
        self.assertEqual(last_name, self.user_data['last_name'])
        self.assertEqual(birthday, self.user_data['birthday'])
        self.assertEqual(telephone, self.user_data['telephone'])

        # User finds logout link of navbar and clicks on it
        self.browser.find_element(value='id_navbar').find_element(value='id_logout_link').click()

        # User inputs his credential data and click on sing in
        self.wait_for(lambda: self.browser.find_element(value='id_login_form'))

        # User see login link of navbar
        self.browser.find_element(value='id_navbar').find_element(value='id_login_link')
