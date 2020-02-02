from django.test import TestCase, Client
from django.db.utils import IntegrityError
from api.models import ShortenedUrl
import json

class ShortenedUrlTestCase(TestCase):
	def test_save(self):
		url = "google.com"
		slug = "i_like_bananas"
		self.assertEqual(ShortenedUrl.objects.count(), 0)
		ShortenedUrl.objects.create(url=url, slug=slug)
		self.assertEqual(ShortenedUrl.objects.count(), 1)
		shortened_url = ShortenedUrl.objects.first()
		self.assertEqual(shortened_url.url, url)
		self.assertEqual(shortened_url.slug, slug)

	def test_save_slug_not_unique(self):
		url = "google.com"
		different_url = "wikipedia.com"
		slug = "i_like_bananas"
		self.assertEqual(ShortenedUrl.objects.count(), 0)
		ShortenedUrl.objects.create(url=url, slug=slug)
		self.assertEqual(ShortenedUrl.objects.count(), 1)

		with self.assertRaises(Exception) as error:
			ShortenedUrl.objects.create(url=different_url, slug=slug)
		self.assertEqual(IntegrityError, type(error.exception))


	def test_save_autogenerate_slug(self):
		url = "google.com"
		self.assertEqual(ShortenedUrl.objects.count(), 0)
		shortened_url = ShortenedUrl.objects.create(url=url)
		self.assertEqual(ShortenedUrl.objects.count(), 1)
		self.assertIsNotNone(shortened_url.slug)


class CreateShortenedUrlViewTestCase(TestCase):

	def test_post(self):
		url = "banana.com"
		slug = "woooo"
		client = Client()
		response = client.post('/api/urls', {"url": url, "slug": slug})
		self.assertEqual(json.loads(response.content)["result"]["slug"], slug)
		self.assertEqual(response.status_code, 200)


	def test_post_without_slug(self):
		url = "banana.com"
		client = Client()
		response = client.post('/api/urls', {"url": url})
		self.assertIsNotNone(json.loads(response.content)["result"]["slug"])
		self.assertEqual(response.status_code, 200)

	def test_post_without_url(self):
		client = Client()
		response = client.post('/api/urls')
		self.assertIsNotNone(json.loads(response.content)["result"]["errors"])
		self.assertEqual(response.status_code, 400)


	def test_get(self):
		client = Client()
		response = client.get('/api/urls')
		self.assertEqual(response.status_code, 404)
