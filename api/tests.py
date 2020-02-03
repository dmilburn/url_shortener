from django.test import TestCase, Client
from django.db.utils import IntegrityError
from api.models import ShortenedUrl, VisitedUrl
import json
from datetime import timedelta
from django.utils import timezone

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


class RedirectShortenedUrlViewTestCase(TestCase):

	def test_get_success(self):
		url = "http://banana.com"
		slug = "woooo"
		self.assertEqual(VisitedUrl.objects.all().count(), 0)
		shortened_url = ShortenedUrl.objects.create(url=url, slug=slug)
		client = Client()
		response = client.get(f'/{slug}')
		self.assertRedirects(response, url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=False)
		self.assertEqual(VisitedUrl.objects.filter(shortened_url=shortened_url).count(), 1)

	def test_get_404(self):
		slug = "woooo"
		client = Client()
		response = client.get(f'/{slug}')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(VisitedUrl.objects.all().count(), 0)

class ReadShortenedUrlViewTestCase(TestCase):

	def test_get_no_visits(self):
		url = "http://banana.com"
		slug = "woooo"
		shortened_url = ShortenedUrl.objects.create(url=url, slug=slug)
		client = Client()
		response = client.get(f'/api/urls/{slug}')
		expected_response = {
			"result": {
				"created_on": str(shortened_url.created_on),
				"total_visits": 0,
				"visit_count_by_day": {},
			}
		}
		self.assertEqual(json.loads(response.content), expected_response)

	def test_get_with_visits(self):
		url = "http://banana.com"
		slug = "woooo"
		shortened_url = ShortenedUrl.objects.create(url=url, slug=slug)
		day_1 = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
		day_2 = day_1 + timedelta(days=1)
		visits = []
		for _ in range(3):
			visits.append(VisitedUrl.objects.create(shortened_url=shortened_url))

		visits[0].created_on = day_1
		visits[0].save()

		for visit in visits[1:]:
			visit.created_on = day_2
			visit.save()

		client = Client()
		response = client.get(f'/api/urls/{slug}')
		expected_response = {
			"result": {
				"created_on": str(shortened_url.created_on),
				"total_visits": 3,
				"visit_count_by_day": {str(day_1): 1, str(day_2): 2},
			}
		}

		self.assertEqual(json.loads(response.content), expected_response)

	def test_get_404(self):
		slug = "woooo"
		client = Client()
		response = client.get(f'/api/urls/{slug}')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(VisitedUrl.objects.all().count(), 0)