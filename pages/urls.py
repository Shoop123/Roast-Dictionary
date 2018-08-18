from django.conf.urls import url

from .views import (
	about,
	terms,
	privacy
)

urlpatterns = [
	url(r'^about/$', about),
	url(r'^terms/$', terms),
	url(r'^privacy/$', privacy),
]