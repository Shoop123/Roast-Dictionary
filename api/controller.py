import json
from roasts import models, controller
from keys import controller as keys_controller
from users import controller as users_controller
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from random import randint
from api.utils import textToNumber, numberToText

def search(keyword):
	if keyword == '':
		keys = models.Key.objects.all().order_by('created_at')[:10]
	else:
		keys = models.Key.objects.filter(name__icontains=keyword)

		if keys.count() > 0:
			keys = keys[:10]
		else:
			results = {
				'keys': []
			}

	results = {
		'keys': []
	}

	for key in keys:
		info = {
			'id': key.id,
			'name': key.name,
			'new_value': key.name
		}

		results['keys'].append(info)

	info = {
		'id': keyword,
		'name': "Add new keyword",
		'new_value': keyword
	}

	results['keys'].append(info)
	

	return json.dumps(results)

def delete_roast(roast_id):
	models.Roast.objects.filter(id=roast_id).delete()

def main_search(keyword):
	keys = models.Key.objects.filter(name__icontains=keyword)
	results = {
		'keys': []
	}

	for key in keys:
		info = {
			'id': key.id,
			'name': key.name
		}

		results['keys'].append(info)

	return json.dumps(results)

def update_rating(user_id, id, rating):
	new_rating = {
		'up': 0,
		'down': 0,
		'total': 0,
		'roast': '',
		'error': ''
	}

	check = models.Roast.objects.filter(id=id)

	if not check.exists():
		new_rating['error'] = 'Roast with ID ' + str(id) + ' does not exist'
		return json.dumps(new_rating)

	roast = check[0]

	new_rating['roast'] = roast.body

	if rating != '1' and rating != '-1':
		new_rating['up'] = get_rating_count(roast, 1)
		new_rating['down'] = get_rating_count(roast, -1)
		new_rating['error'] = 'Invalid rating (' + str(rating) + ')'
		new_rating['total'] = roast.total_rating
		return json.dumps(new_rating)

	rating = int(rating)

	possible_ratings = models.Rating.objects.filter(roast=roast, user=user_id)

	if possible_ratings.count() == 1:
		if possible_ratings[0].rating == rating:
			possible_ratings.delete()

			up = get_rating_count(roast, 1)
			down = get_rating_count(roast, -1)

			roast.total_rating = up - down

			new_rating['up'] = up
			new_rating['down'] = down
			new_rating['total'] = roast.total_rating
		else:
			possible_ratings[0].rating=rating

			up = get_rating_count(roast, 1)
			down = get_rating_count(roast, -1)

			roast.total_rating = up - down

			new_rating['up'] = up
			new_rating['down'] = down
			new_rating['total'] = roast.total_rating

		roast.save(update_fields=['total_rating'])

		return json.dumps(new_rating)
	elif possible_ratings.count() == 0:
		models.Rating(user=user_id, roast=roast, rating=rating).save()

		up = get_rating_count(roast, 1)
		down = get_rating_count(roast, -1)

		roast.total_rating = up - down

		new_rating['up'] = get_rating_count(roast, 1)
		new_rating['down'] = get_rating_count(roast, -1)
		new_rating['total'] = roast.total_rating

		roast.save(update_fields=['total_rating'])

		return json.dumps(new_rating)
	else:
		new_rating['error'] = 'There seems to be an error with the rating from this user'
		return json.dumps(new_rating)


def get_roast_ids(count):
	roasts = models.Roast.objects.all()[:count]

	roasts_dict = {
		'roasts': []
	}

	for roast in roasts:
		current_roast = {
			'body': roast.body,
			'id': roast.id
		}

		roasts_dict['roasts'].append(current_roast)

	return json.dumps(roasts_dict)

def get_roast_rating(id):
	roasts = models.Roast.objects.filter(id=id)

	if roasts.count() == 0:
		return json.dumps({})
	
	roast = roasts[0]

	ratings = models.Rating.objects.filter(roast=roast)

	rating_dict = {
		'rating': 0,
		'users': [],
		'roast': roast.body
	}

	for rating in ratings:
		rating_dict['rating'] += rating.rating
		rating_dict['users'].append(rating.user.username)

	rating_dict['users'] = list(set(rating_dict['users']))

	return json.dumps(rating_dict)

def get_rating_count(roast, rating):
	return models.Rating.objects.filter(roast=roast, rating=rating).count()

def get_roast_by_id(id):
	roast_dict = {
		'roast': '',
		'rating': 0,
		'keys': [],
		'error': ''
	}

	if not id.isdigit():
		roast_dict['error'] = 'Invalid ID'
		return json.dumps(roast_dict)
	
	id = int(id)

	roasts = models.Roast.objects.filter(id=id)

	if roasts.count() == 0:
		roast_dict['error'] = 'Roast with ID ' + str(id) + ' does not exist'
		return json.dumps(roast_dict)

	roast = models.Roast.objects.get(id=id)

	roast_dict['roast'] = roast.body

	ratings = models.Rating.objects.filter(roast=roast)

	for rating in ratings:
		roast_dict['rating'] += rating.rating

	for key in roast.keys.all():
		roast_dict['keys'].append(key.name)

	return json.dumps(roast_dict)

def repopulate_db():
	AMOUNT = 15

	models.Key.objects.all().delete()
	models.Roast.objects.all().delete()
	models.Rating.objects.all().delete()

	user = User.objects.get(username='testuser')

	up = False

	for i in range(AMOUNT):
		rating = -1
		if up: 
			rating = 1
			up = False
		else:
			up = True

		models.Key(name='key_' + str(AMOUNT-i)).save()
		roast = models.Roast(body='roast_' + str(AMOUNT-i), total_rating=rating)
		roast.save()
		models.Rating(user=user, roast=roast, rating=rating).save()

	keys = models.Key.objects.all()
	roasts = models.Roast.objects.all()
	ratings = models.Rating.objects.all()

	for i in range(len(roasts)):
		roast = roasts[i]

		for j in range(i):
			roast.keys.add(keys[j])

		roast.save()

	data = {
		'keys': list(keys.values_list('name', flat=True)),
		'roasts': list(roasts.values_list('body', flat=True)),
		'ratings': list(ratings.values_list('rating', flat=True))
	}

	return json.dumps(data)

def get_keys(username, user_id, exclude_list, first_roast_body):
	return json.dumps(controller.get_home(username, user_id, exclude_list, first_roast_body))

def get_roasts_for_key(page, key_name, username):
	return json.dumps(keys_controller.get_roasts(page, key_name, username))

def get_roasts_for_user(poster_username, viewer_username, page):
	return json.dumps(users_controller.get_user_roasts(poster_username, viewer_username, page))

def get_user(id):
	return users_controller.get_user(id)