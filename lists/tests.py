from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

	def test_root_url_resolves_to_host_page(self):

		found = resolve('/')
		self.assertEqual(found.func,home_page)

	def test_uses_home_template(self):

		response = self.client.get('/')
		self.assertTemplateUsed(response,'home.html')

	def test_can_save_a_POST_request(self):

		response = self.client.post(
			'/',
			data={
					'item_text':'A new list item'
				}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_can_redirect_after_POST_request(self):
		response = self.client.post(
			'/',
			data={
					'item_text':'A new list item'
				}
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_displays_all_list_items(self):

		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/')

		self.assertIn('itemey 1', response.content.decode())
		self.assertIn('itemey 2', response.content.decode())