from django.db import models
import random
import string
from django.db.models.functions import TruncDay


class ShortenedUrl(models.Model):
	slug = models.SlugField(unique=True, max_length=255, blank=True)
	url = models.URLField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = ShortenedUrl.generate_slug()
		super().save(*args, **kwargs)

	def visit_count_by_day(self):
		grouped_visits = self.visited_urls.all().annotate(date=TruncDay('created_on')).values("date").annotate(total=models.Count("date"))
		formatted_visits = {}
		for visits in grouped_visits:
			formatted_visits[str(visits["date"])] = visits["total"]

		return formatted_visits

	@classmethod
	def generate_slug(cls):
		generated_slug = None
		while not generated_slug:
			random_slug = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
			if not ShortenedUrl.objects.filter(slug=random_slug).exists():
				generated_slug = random_slug

		return generated_slug



class VisitedUrl(models.Model):
	shortened_url = models.ForeignKey(ShortenedUrl, on_delete=models.CASCADE, related_name="visited_urls")
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
