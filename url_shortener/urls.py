from django.urls import include, path
from api.views import redirect_slug

urlpatterns = [
	path('api/', include('api.urls')),
	path('<str:slug>', redirect_slug)
]
