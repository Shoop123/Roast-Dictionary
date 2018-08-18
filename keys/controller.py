from django.core.paginator import Paginator
from roasts import models
import json

def get_roasts(page, key_name, username):
	key_options = models.Key.objects.filter(name=key_name)

	DEFAULT = 10

	keys_dict = {
		'roasts': []
	}

	if key_options.count() > 0:
		key = key_options[0]
	else:
		return json.dumps(keys_dict)

	keys_dict['key_id'] = key.id

	roasts = key.roast_set.all()	

	paginator = Paginator(roasts, DEFAULT)

	if page > paginator.num_pages:
		return json.dumps(keys_dict)

	if page >= paginator.num_pages:
		keys_dict['end'] = True
	else:
		keys_dict['end'] = False

	requested_page = paginator.page(page)

	roasts_in_page = requested_page.object_list

	for roast in roasts_in_page:
		if roast.user == None:
			roast_username = 'Anonymous'
			user_id = -1
		else:
			roast_username = roast.user.username
			user_id = roast.user.id

		ratings = models.Rating.objects.filter(roast=roast)

		other_keys_query_set = list(roast.keys.all())

		other_keys = []

		for other_key in other_keys_query_set:
			if other_key.name != key_name:
				other_keys.append(other_key.name)

		total = roast.total_rating

		rated = 0

		user_rating = ratings.filter(user__username=username)

		if user_rating.exists():
			rated = user_rating.get().rating

		roast_info = {
			'id': roast.id,
			'body': roast.body,
			'user_id': user_id,
			'user': roast_username,
			'rating': total,
			'rated': rated,
			'keys': other_keys
		}

		keys_dict['roasts'].append(roast_info)

	return keys_dict