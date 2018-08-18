from django.conf.urls import url

from .views import (
	post
)

urlpatterns = [
    url(r'^create/$', post),
]