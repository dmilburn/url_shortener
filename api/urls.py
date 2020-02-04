from django.urls import path
from api.views import create_shortened_urls, view_shortened_urls

urlpatterns = [
	path('urls', create_shortened_urls),
	path('urls/<str:slug>', view_shortened_urls),
]
