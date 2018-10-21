from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# https://docs.djangoproject.com/en/2.1/topics/testing/tools/#provided-test-case-classes
# https://docs.python.org/3.5/library/functions.html#super


class NewVistorTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
        self.selenium.get(self.live_server_url)
        self.fail("Finish the test.")
