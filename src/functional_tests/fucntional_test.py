from time import sleep, time
from unittest import TestLoader

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAITED_TIME = 10


def wait(fn):
    def wrapper(*args, **kwargs):
        start_time = time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAITED_TIME:
                    raise e
                sleep(0.5)

    return wrapper


class FunctionalTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = self.create_browser()

    def tearDown(self) -> None:
        if self._is_last_test():
            self.browser.quit()
        else:
            self.browser.close()

    def _is_last_test(self):
        loader = TestLoader()
        last_test = list(loader.loadTestsFromTestCase(self.__class__))[-1]
        if self._testMethodName == last_test._testMethodName:
            return True
        return False

    @staticmethod
    def create_browser():
        options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(options=options)
        return browser

    @wait
    def wait_for(self, fn):
        return fn()
