# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.brower = webdriver.Firefox()


    def tearDown(self):
        self.brower.quit()


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Eidth has heard about a cool new online to-do app. She goes to check out its homepage.
        self.brower.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.brower.title)
        header_text = self.brower.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.brower.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box (Edith's hobby is typing fly-fishing lures).
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)

        # selenium.common.exceptions.StaleElementReferenceException:
        import time
        time.sleep(2)

        table = self.brower.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        # We apply a generator expression inside any.
        self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows), 'New item did not appear in table.')

        # There is still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical).
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list.

        # Edith wonders whether the site will remember her list. Then she sees that
        # the site has generated a unique URL for her -- there is some explanatory text
        # to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.


if __name__ == '__main__':
    unittest.main()
