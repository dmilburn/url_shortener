from django.forms import ModelForm
from api.models import ShortenedUrl

class ShortenedUrlForm(ModelForm):
	class Meta:
		model = ShortenedUrl
		fields = ["url", "slug"]