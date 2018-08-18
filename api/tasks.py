from __future__ import absolute_import, unicode_literals
from celery import shared_task
from roasts.models import Roast, Rating, RoastsOfTheDay
from django.db.models import Sum
import random, pickle, os

@shared_task
def set_roasts_of_day():
	AMOUNT = 5
	MIN_RATING = 0

	clean_roasts = Roast.objects.filter(total_rating__gte=MIN_RATING, roast_of_the_day=False)

	if clean_roasts.count() <= AMOUNT:
		Roast.objects.filter(total_rating__gte=MIN_RATING, roast_of_the_day=True).update(roast_of_the_day=False)
		clean_roasts = Roast.objects.filter(total_rating__gte=MIN_RATING, roast_of_the_day=False)

	indices = random.sample(range(0, clean_roasts.count()), AMOUNT)

	selected_roasts = []

	# need to have 2 for loops because querysets suck
	for index in indices:
		selected_roasts.append(clean_roasts[index])

	for selected_roast in selected_roasts:
		selected_roast.roast_of_the_day = True
		selected_roast.save(update_fields=['roast_of_the_day'])

	if RoastsOfTheDay.objects.count() != 1:
		RoastsOfTheDay.objects.all().delete()

		RoastsOfTheDay(
				roast_1=selected_roasts[0],
				roast_2=selected_roasts[1],
				roast_3=selected_roasts[2],
				roast_4=selected_roasts[3],
				roast_5=selected_roasts[4]
			).save()
	else:
		roasts_of_the_day = RoastsOfTheDay.objects.get()

		indices = random.sample(range(0, clean_roasts.count()), AMOUNT)

		roasts_of_the_day.roast_1 = selected_roasts[0]
		roasts_of_the_day.roast_2 = selected_roasts[1]
		roasts_of_the_day.roast_3 = selected_roasts[2]
		roasts_of_the_day.roast_4 = selected_roasts[3]
		roasts_of_the_day.roast_5 = selected_roasts[4]

		roasts_of_the_day.save()