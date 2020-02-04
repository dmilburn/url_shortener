from django.urls import include, path
from api.views import redirect_slug

'''
Future devs: be wary of adding new URLs to this file without having them nested like the "api" paths
In order to redirect any short link, we have to match any string at the highest level
'''

urlpatterns = [
	path('api/', include('api.urls')),
	path('<str:slug>', redirect_slug)
]
