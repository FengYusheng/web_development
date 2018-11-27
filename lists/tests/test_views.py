# -*- coding: utf-8 -*-
from unittest import skip

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm

# Create your tests here.

class HomePageTest(TestCase):
    maxDiff = None
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    @skip
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'form':ItemForm()})
        # print(expected_html)
        # TODO: remove csrf, https://stackoverflow.com/questions/34629261/django-render-to-string-ignores-csrf-token#34629713
        self.assertMultiLineEqual(response.content.decode(), expected_html)


    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/{0}/'.format(correct_list.id))
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'ohter list item 2')


    def test_pass_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)


    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{0}/'.format(correct_list.id),
            data = {'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{0}/'.format(correct_list.id),
            data = {'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{0}/'.format(correct_list.id))


    def test_validation_errors_and_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/{0}/'.format(list_.id), data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        # self.assertEqual(response.context['error'], "You can't have an empty list item")


    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0}/'.format(list_.id))
        self.assertIsInstance(response.context['form'], ItemForm)



class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item.'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item.')


    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item.'}
        )

        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/{0}/'.format(new_list.id))


    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "You can&#39;t have an empty list item")


    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


    def test_input_passes_from_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
