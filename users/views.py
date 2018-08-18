from django.shortcuts import render, redirect
from django.http import HttpResponse
from roasts import models
from .forms import SignUpForm, LoginForm, PasswordChangeForm, AccountForm
import controller

from roasts.controller import compile_roast_of_the_day_dict

HOME = '../../'
SETTINGS = HOME + 'users/settings/'

def side_bar_log_in_info(request):
	sign_up_form = None
	log_in_form = None

	if request.method == 'POST':
		if 'email' in request.POST:
			sign_up_form = SignUpForm(request.POST)

			if sign_up_form.is_valid():
				username = sign_up_form.cleaned_data.get('username')
				email = sign_up_form.cleaned_data.get('email')
				password = sign_up_form.cleaned_data.get('password')

				controller.sign_up(username, email, password)
				controller.log_in_account(request, username, password)
		else:
			log_in_form = LoginForm(request.POST)

			if log_in_form.is_valid():
				username = log_in_form.cleaned_data.get('username')
				password = log_in_form.cleaned_data.get('password')

				controller.log_in_account(request, username, password)
	
	if not sign_up_form:
		sign_up_form = SignUpForm(None)

	if not log_in_form:
		log_in_form = LoginForm(None)

	return sign_up_form, log_in_form

def sign_up(request):
	form = SignUpForm(request.POST or None)

	context = {
		'form': form
	}

	if form.is_valid():
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')

		controller.sign_up(username, email, password)
		controller.log_in_account(request, username, password)

		return redirect(HOME)

	return render(request, 'users/sign_up.html', context)

def log_in(request):
	if request.user.is_authenticated():
		return redirect(HOME)

	form = LoginForm(request.POST or None)

	context = {
		'form': form
	}

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')

		controller.log_in_account(request, username, password)

		return redirect(HOME)

	return render(request, 'users/log_in.html', context)

def log_out(request):
	if request.user.is_authenticated():
		controller.log_out_account(request)
	
	return redirect(HOME)

def list_users(request):
	return HttpResponse(controller.get_users())

def profile(request, id):
	sign_up_form, log_in_form = side_bar_log_in_info(request)
	user = controller.get_user(id)

	if user is None:
		return redirect(HOME)

	context = controller.get_user_roasts(user, request.user.username, 1)
	context['username'] = user.username
	context['roasts_of_the_day'] = compile_roast_of_the_day_dict()
	context['sign_up_form'] = sign_up_form
	context['log_in_form'] = log_in_form

	return render(request, 'users/profile.html', context)

def settings(request):
	if request.user.is_authenticated():
		form = AccountForm(request.POST or None, user=request.user, initial={'username': request.user.username, 'email': request.user.email})

		if form.is_valid():
			controller.update_acccount(request.user.username, form.cleaned_data.get('username'), form.cleaned_data.get('email'))
			return redirect(SETTINGS)

		context = {
			'form': form
		}

		return render(request, 'users/settings.html', context)
	else:
		return redirect(HOME)

def change_password(request):
	if request.user.is_authenticated():
		form = PasswordChangeForm(request.POST or None, user=request.user)

		if form.is_valid():
			controller.update_password(request, request.user.username, form.cleaned_data.get('new_password'))
			return redirect(SETTINGS)

		context = {
			'form': form
		}

		return render(request, 'users/change_password.html', context)
	else:
		redirect(HOME)

def edit(request):
	context = {
		'user': request.user
	}