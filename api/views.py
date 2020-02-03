from django.shortcuts import render
from api.forms import ShortenedUrlForm
from django.http import JsonResponse
from django.shortcuts import redirect
from api.models import ShortenedUrl, VisitedUrl
import json

def create_shortened_urls(request):
	if request.method == 'POST':
		shortened_url = None

		slug = request.POST.get("slug")
		url = request.POST.get("url")

		if url and not slug:
			shortened_url = ShortenedUrl.objects.filter(url=url).first()

		if not shortened_url:
			shortened_url_form = ShortenedUrlForm(request.POST)
			if shortened_url_form.is_valid():
				shortened_url = shortened_url_form.save()

		if shortened_url:
			return JsonResponse({"result": {"success": True, "slug": shortened_url.slug}})
		return JsonResponse({"result": {"success": False, "errors": shortened_url_form.errors}}, status=400)

	return JsonResponse404()

def redirect_slug(request, slug):
	if request.method == 'GET':
		shortened_url = ShortenedUrl.objects.filter(slug=slug).first()
		if shortened_url:
			VisitedUrl.objects.create(shortened_url=shortened_url)
			return redirect(shortened_url.url)

	return JsonResponse404()

def view_shortened_urls(request, slug):
	if request.method == 'GET':
		shortened_url = ShortenedUrl.objects.filter(slug=slug).first()
		if shortened_url:
			return JsonResponse({"result": {
					"created_on": str(shortened_url.created_on),
					"total_visits": shortened_url.visited_urls.count(),
					"visit_count_by_day": shortened_url.visit_count_by_day(),
				}
			})
	return JsonResponse404()

def JsonResponse404():
	return JsonResponse({"result": "This page does not exist"}, status=404)