from django.conf.urls import url
from api.utils import VALID_CHARS

KEY_RANGE = r'^(?P<key>[\ a-zA-Z0-9' + VALID_CHARS +']+)/$'

from .views import (
	key_page
)

urlpatterns = [
	url(KEY_RANGE, key_page)
]