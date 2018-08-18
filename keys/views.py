from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError

from users.views import side_bar_log_in_info

from roasts import models
from roasts.controller import compile_roast_of_the_day_dict

import controller

def key_page(request, key):
	sign_up_form, log_in_form = side_bar_log_in_info(request)

	page = 1

	if 'page' in request.GET:
		if request.GET['page'].isdigit() and int(request.GET['page']) > 0:
			page = int(request.GET['page'])

	username = 'Anonymous'

	if request.user.is_authenticated():
		username = request.user.username

	roasts = controller.get_roasts(page, key, username)

	context = {
		'roasts': roasts,
		'key': key,
		'sign_up_form': sign_up_form,
		'log_in_form': log_in_form,
		'roasts_of_the_day': compile_roast_of_the_day_dict()
	}

	return render(request, 'keys/key_page.html', context)