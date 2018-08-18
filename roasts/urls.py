from django.conf.urls import url
from django.contrib import admin
from api.utils import VALID_CHARS

from .views import (
	home,
	add_roast,
	edit_roast,
	takealook,
)

urlpatterns = [
	url(r'^$', home),
	url(r'^add_roast/$', add_roast),
	url(r'^edit_roast/$', edit_roast),
	url(r'^takealook/(?P<roast_id>\d+)/$', takealook)
]