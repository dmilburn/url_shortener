from django.shortcuts import render
from api.forms import ShortenedUrlForm
from django.http import JsonResponse


def create_shortened_urls(request):
	errors = []
	if request.method == 'POST':
		shortened_url_form = ShortenedUrlForm(request.POST)
		if shortened_url_form.is_valid():
			shortened_url = shortened_url_form.save()
			return JsonResponse({"result": {"success": True, "slug": shortened_url.slug}})
		return JsonResponse({"result": {"success": False, "errors": shortened_url_form.errors}}, status=400)
	else:
		return JsonResponse({"result": "This page does not exist"}, status=404)
