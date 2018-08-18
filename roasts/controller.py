import models, random
from django.db.models import Sum
from api import tasks
from django.contrib.auth.models import User
from api.utils import create_valid_keys, valid_roast
from django.http.request import QueryDict, MultiValueDict
from django.shortcuts import get_object_or_404
from urllib import quote_plus

todays_roasts = []

def get_home(username, user_id, exclude_list, focus_roast_id):
	roasts_qs = models.Roast.objects.filter(total_rating__gte=-5)
	keys = models.Key.objects.filter(roast__in=roasts_qs).distinct().exclude(id__in=exclude_list)

	DEFAULT = 10

	random_keys = randomize_query_order(keys, DEFAULT)

	end = len(exclude_list) + len(random_keys) >= keys.count()

	focus_roast = None

	if focus_roast_id is not None:
		posibilities = models.Roast.objects.filter(id=focus_roast_id)

		if posibilities.count() > 0:
			focus_roast = get_roast_summary(posibilities[0], None, user_id)
			focus_roast['facebook'] = get_facebook_url(str(posibilities[0].id))
			focus_roast['twitter'] = get_twitter_url(str(posibilities[0].id))

	keys_dict = {
		'keys': [],
		'focus_roast': focus_roast,
		'end': end
	}

	MAX_ROASTS = 5

	for key in random_keys:
		clean_roasts = key.roast_set.filter(total_rating__gte=-5)

		roasts = randomize_query_order(clean_roasts, MAX_ROASTS)

		organised_roasts = []

		for roast in roasts:
			roast_summary = get_roast_summary(roast, key, user_id)
			roast_summary['facebook'] = get_facebook_url(str(roast.id))
			roast_summary['twitter'] = get_twitter_url(str(roast.id))

			organised_roasts.append(roast_summary)

		keys_dict['keys'].append({
			'id': key.id,
			'name': key.name,
			'roasts': organised_roasts
		})

	return keys_dict

def get_facebook_url(roast_body):
	link = 'https://www.facebook.com/sharer/sharer.php?u='
	url = 'https://roastdictionary.com?focus-roast=' + roast_body

	return link + url

def get_twitter_url(roast_body):
	link = 'http://twitter.com/intent/tweet?text='
	text = 'Check+out+this+savage+roast&'
	via = 'via=RoastDictionary&'
	url = 'url=https://roastdictionary.com?focus-roast=' + roast_body + '&'
	hashtags = 'hashtags=roastdictionary&'
	short_url_length_https = 'short_url_length=23'

	return link + text + via + url + hashtags + short_url_length_https

def get_roast_summary(roast, key, user_id):
	if roast.user == None:
		roast_username = 'Anonymous'
		roast_user_id = 0
	else:
		roast_username = roast.user.username
		roast_user_id = roast.user.id

	ratings = models.Rating.objects.filter(roast=roast)

	if key is not None:
		other_keys_query_set = list(roast.keys.all().exclude(name=key.name)[:5])
	else:
		other_keys_query_set = list(roast.keys.all()[:5])

	other_keys = []

	for other_key in other_keys_query_set:
		other_keys.append(other_key.name)

	rated = 0

	user_rating = ratings.filter(user=user_id)

	if user_rating.exists():
		rated = user_rating.get().rating

	roast_dict = {
		'user': roast_username,
		'user_id': roast_user_id,
		'roast': roast.body,
		'id': roast.id,
		'total': roast.total_rating,
		'rated': rated,
		'other_keys': other_keys
	}

	return roast_dict

def compile_roast_of_the_day_dict():
	if models.RoastsOfTheDay.objects.count() != 1:
		tasks.set_roasts_of_day()

	roasts_of_the_day_model = models.RoastsOfTheDay.objects.get()

	roasts_of_the_day = [
		get_roast_of_the_day_info(roasts_of_the_day_model.roast_1),
		get_roast_of_the_day_info(roasts_of_the_day_model.roast_2),
		get_roast_of_the_day_info(roasts_of_the_day_model.roast_3),
		get_roast_of_the_day_info(roasts_of_the_day_model.roast_4),
		get_roast_of_the_day_info(roasts_of_the_day_model.roast_5)
	]

	return roasts_of_the_day

def get_roast_of_the_day_info(roast):
	username = 'Anonymous'
	user_id = -1

	if roast.user is not None:
		username = roast.user.username
		user_id = roast.user.id

	roast_of_the_day = {
		'username': username,
		'user_id': user_id,
		'roast': roast.body
	}

	return roast_of_the_day

def randomize_query_order(q, number):
	random_list = []

	total_count = q.count()

	if number > total_count:
		number = total_count

	while len(random_list) < number:
		index = random.randint(0, q.count() - 1)

		obj = q[index]
		random_list.append(obj)

		q = q.exclude(id=obj.id)

	return random_list

def filter_bad_keys(all_keys):
	good_results = []

	all_keys.filter()

	for key in all_keys:
		roasts = key.roast_set.all()
		good_roasts = []

		for roast in roasts:
			ratings = models.Rating.objects.filter(roast=roast)
			avg = ratings.aggregate(Sum('rating'))

			if avg['rating__sum'] is None or avg['rating__sum'] > -5:
				good_roasts.append(roast)

		if len(good_roasts) > 0:
			result = {
				'key': key,
				'roasts': good_roasts
			}

			good_results.append(result)

	return good_results

def get_set_post_request(post, edit=False):
	created, ids, key_errors = create_valid_keys(post.getlist('keys'))

	is_valid, added_keys = valid_roast(post.getlist('body')[0], ids)

	if is_valid or len(added_keys) == 0:
		roast_exists = 'f'

		if not is_valid and not edit:
			roast_exists = 't'

		new_post = {
			'keys': ids, 
			'body': post.getlist('body'),
			'csrfmiddlewaretoken': post.getlist('csrfmiddlewaretoken'),
			'key_errors': key_errors,
			'roast_exists': [roast_exists]
		}

		post_request = QueryDict('', mutable=True)
		post_request.update(MultiValueDict(new_post))

		return post_request

def get_roast_info(roast_id):
	roast = get_object_or_404(models.Roast, id=roast_id)

	keys = roast.keys.all().values_list('name', flat=True)

	if roast.user is None:
		username = 'Anonymous'
	else:
		username = roast.user.username

	print keys

	roast_info = {
		'roast': roast.body,
		'id': roast.id,
		'username': username,
		'rating': roast.total_rating,
		'keys': keys
	}

	return roast_info