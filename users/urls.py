from django.conf.urls import include, url
from django.contrib.auth import views
from api.utils import VALID_CHARS
from forms import CustomPasswordResetForm

KEY_RANGE = r'^(?P<id>[\ a-zA-Z0-9' + VALID_CHARS +']+)/$'

from .views import (
	sign_up,
	list_users,
	log_in,
	log_out,
	profile,
	edit,
	settings,
	change_password,
)

urlpatterns = [
	url(r'^sign_up/$', sign_up),
	url(r'^log_in/$', log_in),
	url(r'^log_out/$', log_out),
	url(r'^settings/$', settings),
	url(r'^change_password/$', change_password),
	url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^list_users/$', list_users),
	url(KEY_RANGE, profile),
	url(r'^edit/$', edit),

	url(r'^password/reset/$', 
		views.password_reset, 
		{'post_reset_redirect' : '/users/password/reset/done/',
		'password_reset_form': CustomPasswordResetForm},
		name="password_reset"),
	url(r'^password/reset/done/$',
		views.password_reset_done),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', 
		views.password_reset_confirm,
		{'post_reset_redirect' : '/users/password/done/'}, 
		name='password_reset_confirm'),
	url(r'^password/done/$', 
		views.password_reset_complete)
]
