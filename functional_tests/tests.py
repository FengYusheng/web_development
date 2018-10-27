from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

# https://docs.djangoproject.com/en/2.1/topics/testing/tools/#provided-test-case-classes
# https://docs.python.org/3.5/library/functions.html#super


class NewVistorTest(LiveServerTestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.browser = webdriver.Firefox()
    #     cls.browser.implicitly_wait(10)
    #
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.browser.quit()
    #     super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)


    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > 10:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.live_server_url)
        # print(self.live_server_url)

        # She notices the page title and header mention to-do listsself.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # she is invited to enter a to-do item straight away.
        inpubtox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inpubtox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)
        inpubtox.send_keys('Buy peacock feathers')
        inpubtox.send_keys(Keys.ENTER)
        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, r'/lists/.+')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "use peacock feathers to make a fly" (Edith is
        # very methodical)

        # Retreive the input box again since redirecting
        inpubtox = self.browser.find_element_by_id('id_new_item')
        inpubtox.send_keys('Use peacock feathers to make a fly')
        inpubtox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list.
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', body_text)
        self.assertNotIn('2: Use peacock feathers to make a fly', body_text)

        # Francis starts a new list by entering a new item. He is less interesting
        # than Edith.
        inpubtox = self.browser.find_element_by_id('id_new_item')
        inpubtox.send_keys('Buy milk')
        inpubtox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Eidth wonders whether the site wiil remember her list. Then she sees
        # that the site has gernerate a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail("Finish the test.")

        # She visits that URL - her to-do list is still there.

        # Satisfiled, she goes backk to sleep.
