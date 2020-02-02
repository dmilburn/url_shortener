from django.test import TestCase
from django.db.utils import IntegrityError
from api.models import ShortenedUrl

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