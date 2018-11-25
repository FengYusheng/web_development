# -*- coding: utf-8 -*-
# https://docs.djangoproject.com/en/2.1/howto/static-files/
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import time
import sys
import os

# https://docs.djangoproject.com/en/2.1/topics/testing/tools/#provided-test-case-classes
# https://docs.python.org/3.5/library/functions.html#super
#https://www.obeythetestinggoat.com/book/chapter_manual_deployment.html


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        staging_sever = os.environ.get('STAGING_SERVER')
        if staging_sever:
            cls.serverl_url = 'http://' + staging_sever
            return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()


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
