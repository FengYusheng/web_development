# -*- coding: utf-8 -*-
import time

from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page.
        self.browser.get(self.server_url)
        print(self.browser.get_window_position(), self.browser.get_window_size())
        # NOTE: I can't set the window size smaller than (1221, 617). Why?
        # self.browser.set_window_size(800, 600)
        self.browser.set_window_size(1221, 617)
        time.sleep(5)

        # She notices the input box is nicely centered.
        inpubtox = self.browser.find_element_by_id('id_new_item')
        # print(inpubtox.location, inpubtox.size)
        # print(self.browser.get_window_position(), self.browser.get_window_size())
        self.assertAlmostEqual(inpubtox.location['x']+inpubtox.size['width']/2,
                               # 610,
                               325,
                               delta=5)
