from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.template import RequestContext

from users.forms import SignUpForm, LoginForm
from users.views import side_bar_log_in_info

import models, controller
import datetime

from .forms import RoastForm

HOME = '../../'
HOME_PARAM = '?focus-roast='
PROFILE = HOME + 'users/'
LOGIN = HOME + 'users/log_in/'

def home(request):
	sign_up_form, log_in_form = side_bar_log_in_info(request)

	username = 'Anonymous'

	if request.user.is_authenticated():
		username = request.user.username

	focus_roast_id = None

	if 'focus-roast' in request.GET and request.GET['focus-roast'].isdigit():
		focus_roast_id = int(request.GET['focus-roast'])

	keys = controller.get_home(username, request.user.id, [], focus_roast_id)

	now = datetime.datetime.now()

	current_date = iso_8601_format(now)

	context = {
		'keys': keys,
		'sign_up_form': sign_up_form,
		'log_in_form': log_in_form,
		'roasts_of_the_day': controller.compile_roast_of_the_day_dict(),
		'current_date': current_date
	}

	return render(request, 'roasts/home.html', context)

def add_roast(request):
	if request.POST == {}:
		form = RoastForm()
	else:
		post = request.POST.copy()

		post_request = controller.get_set_post_request(post)

		if post_request is not None:
			form = RoastForm(post_request)

			if form.is_valid():
				roast = form.save(commit=False)

				if request.user.is_authenticated():
					roast.user = request.user

				form.save(commit=True)
				roast.save()
				
				return redirect(HOME + HOME_PARAM + str(roast.id))
		else:
			return redirect(HOME)

	context = {
		'form': form,
		'title': 'Create',
		'button_name': 'Create'
	}

	return render(request, 'roasts/add_roast.html', context)

def edit_roast(request):
	if request.user.is_authenticated():
		if 'roast_id' in request.GET:
			roast_id = request.GET['roast_id']

			if not roast_id.isdigit():
				raise Http404("Roast does not exist")

			roast = get_object_or_404(models.Roast, pk=roast_id)

			if roast.user.username != request.user.username:
				raise PermissionDenied

			if request.POST == {}:
				form = RoastForm(instance=roast)
			else:
				post = request.POST.copy()

				post_request = controller.get_set_post_request(post, edit=True)

				form = RoastForm(post_request, instance=roast)

				if post_request is not None:
					if form.is_valid():
						form.save()
						return redirect(PROFILE + str(request.user.id))
				else:
					return redirect(PROFILE + str(request.user.id))

			context = {
				'form': form,
				'title': 'Edit',
				'button_name': 'Update'
			}

			return render(request, 'roasts/add_roast.html', context)
		else:
			raise SuspiciousOperation
	else:
		return redirect(LOGIN)

def takealook(request, roast_id):
	return redirect(HOME + HOME_PARAM + roast_id)
	# sign_up_form, log_in_form = side_bar_log_in_info(request)

	# context = controller.get_roast_info(roast_id)

	# context['sign_up_form'] = sign_up_form
	# context['log_in_form'] = log_in_form
	# context['roasts_of_the_day'] = controller.compile_roast_of_the_day_dict()
	# context['app_url'] = request.path

	# return render(request, 'roasts/takealook.html', context)



def iso_8601_format(dt):
    """YYYY-MM-DDThh:mm:ssTZD (1997-07-16T19:20:30-03:00)"""

    if dt is None:
        return ""

    fmt_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S')
    tz = dt.utcoffset()
    if tz is None:
        fmt_timezone = "+00:00"
    else:
        fmt_timezone = str.format('{0:+06.2f}', float(tz.total_seconds() / 3600))

    return fmt_datetime + fmt_timezone