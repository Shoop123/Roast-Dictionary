from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

import json

from roasts.models import Roast

from django.core.paginator import Paginator

from roasts import models

def get_users():
	users = User.objects.all()

	user_dict = {
		'users': []
	}

	for user in users:
		user_dict['users'].append(user.username)

	return json.dumps(user_dict)

def get_user(id):
	user = User.objects.filter(id=id)

	if user.exists():
		user = user.get()
	else:
		user = None
	
	return user

def sign_up(username, email, password):
	User.objects.create_user(username, email=email, password=password)

def log_in_account(request, username, password):
	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)

def log_out_account(request):
	logout(request)

def update_acccount(old_username, new_username, new_email):
	user = User.objects.get(username=old_username)

	user.username = new_username
	user.email = new_email
	
	user.save()

def update_password(request, username, new_password):
	user = User.objects.get(username=username)

	user.set_password(new_password)

	user.save()
	
	update_session_auth_hash(request, user)

def get_user_roasts(poster_username, viewer_username, page):
	users = User.objects.filter(username=poster_username)

	info = {
		'roasts': []
	}

	if users.exists():
		user_id = users[0]
	else:
		return info

	ITEMS = 10

	roasts = Roast.objects.filter(user=user_id).order_by('created_at')

	paginator = Paginator(roasts, ITEMS)

	if page >= paginator.num_pages:
		info['end'] = True
	else:
		info['end'] = False

	print info['end']

	if page > paginator.num_pages:
		return json.dumps(info)

	roasts_in_page = paginator.page(page)

	requested_page = roasts_in_page.object_list

	if requested_page.exists():
		for roast in requested_page:
			body = roast.body

			roast_username = roast.user.username

			keys = []

			for key in roast.keys.all():
				keys.append(key.name)

			ratings = models.Rating.objects.filter(roast=roast, user__username=viewer_username)

			total = roast.total_rating

			rated = 0

			if ratings.exists():
				rated = ratings.get().rating

			roast_dict = {
				'user': roast_username,
				'roast': roast.body,
				'id': roast.id,
				'total': total,
				'rated': rated,
				'keys': keys
			}

			info['roasts'].append(roast_dict)

	return info