from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from accounts.tests import create_test_user
from functional_tests.fucntional_test import FunctionalTest
from rooms.models import TYPE


class BookingAppTest(FunctionalTest):
    def setUp(self) -> None:
        super().setUp()
        self.check_in = datetime.now() + timedelta(days=1)
        self.check_out = self.check_in + timedelta(days=10)
        self.user_data = {
            'email': 'rick.sanchez@test.com',
            'password': 'qwe123!@#',
            'first_name': 'Rick',
            'last_name': 'Sanchez',
            'birthday': '1958-07-03',
            'telephone': '+38 (050) 000 00 00',
            'persons': '2',
            'type': 0,
            'check_in': str(self.check_in.date()),
            'check_out': str(self.check_out.date()),
        }

    def test_user_can_book_room(self):
        user = create_test_user()
        user.is_confirmed_email = True
        user.save()
        profile = user.profile
        profile.first_name = self.user_data['first_name']
        profile.last_name = self.user_data['last_name']
        profile.birthday = self.user_data['birthday']
        profile.telephone = self.user_data['telephone']
        profile.save()

        # User goes to site to book
        self.browser.get(self.live_server_url)

        # User finds a login link in the navbar and clicks on it
        self.browser.find_element(value='id_navbar').find_element(value='id_login_link').click()

        # User inputs his credential data and click on sing in
        self.wait_for(lambda: self.browser.find_element(value='id_login_form'))

        self.enter_to_input_field(self.user_data['email'], value='id_email')
        self.enter_to_input_field(self.user_data['password'], value='id_password')

        self.browser.find_element(value='id_login_button').click()

        # User follows to account page
        self.wait_for(lambda: self.browser.find_element(value='id_account_form'))

        # User finds a booking link in the navbar and clicks on it
        self.browser.find_element(value='id_navbar').find_element(value='id_booking_link').click()

        # User follows to booking list and sees empty booking list.
        self.wait_for(lambda: self.browser.find_element(value='id_booking_list'))

        text = self.browser.find_element(value='id_empty_list_message').text
        expected_text = "You didn't book room yet"

        self.assertIn(expected_text, text)

        # User click on booking room link.
        self.browser.find_element(value='id_booking_room_link').click()

        # User follows to booking form page and fills necessary field.
        self.wait_for(lambda: self.browser.find_element(value='id_booking_form'))

        # User input two persons
        self.enter_to_input_field(self.user_data['persons'], value='id_persons')

        # User choose economy room type
        dropdown = self.browser.find_element(value='id_type')
        select = Select(dropdown)
        select.select_by_index(self.user_data['type'])

        # User has a child
        checkbox = self.browser.find_element(value='id_is_children')
        checkbox.click()

        # User choose check in date
        self.enter_to_input_field(self.user_data['check_in'], value='id_check_in')

        # User choose check out date
        self.enter_to_input_field(self.user_data['check_out'], value='id_check_out')

        # User clicks on booking button
        self.browser.find_element(value='id_booking_button').click()

        # User follows to booking list page and checks booking data.
        self.wait_for(lambda: self.browser.find_element(value='id_booking_list'))

        card = self.browser.find_element(By.CLASS_NAME, 'card')
        rooms = card.find_element(By.XPATH, value='//p[contains(text(), "Rooms:")]')
        persons = card.find_element(By.XPATH, value='//p[contains(text(), "Persons:")]')
        type = card.find_element(By.XPATH, value='//p[contains(text(), "Type:")]')
        total_price = card.find_element(By.XPATH, value='//p[contains(text(), "Total price:")]')
        has_children = card.find_element(By.XPATH, value='//p[contains(text(), "Has children:")]')
        check_in = card.find_element(By.XPATH, value='//p[contains(text(), "Check in date:")]')
        check_out = card.find_element(By.XPATH, value='//p[contains(text(), "Check out date:")]')

        self.assertIn("Manager doesn't choose room/rooms for you.", rooms.text)
        self.assertIn(self.user_data['persons'], persons.text)
        self.assertIn(TYPE.choices[self.user_data['type']][1], type.text)
        self.assertTrue(has_children.text)
        self.assertIn('-', total_price.text)
        self.assertIn(self.check_in.strftime('%d %b. %Y'), check_in.text)
        self.assertIn(self.check_out.strftime('%d %b. %Y'), check_out.text)
