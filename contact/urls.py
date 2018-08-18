from django.conf.urls import url

from .views import (
	contact,
	thank_you
)

urlpatterns = [
	url(r'^contact/$', contact),
	url(r'^thank_you/$', thank_you),
]