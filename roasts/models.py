from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Key(models.Model):
	name = models.CharField(max_length=20, unique=True)
	created_at = models.DateTimeField(default=timezone.now, editable=False)

	def __unicode__(self):
		return self.name

	class Meta:
		get_latest_by = 'created_at'

class Roast(models.Model):
	body = models.CharField(max_length=200)
	keys = models.ManyToManyField(Key)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
	total_rating = models.IntegerField(default=0, editable=False)
	created_at = models.DateTimeField(default=timezone.now, editable=False)
	roast_of_the_day = models.BooleanField(default=False, editable=False)

	def __unicode__(self):
		return self.body

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	roast = models.ForeignKey(Roast, on_delete=models.CASCADE)
	rating = models.SmallIntegerField(default=0, validators=[MaxValueValidator(1), MinValueValidator(-1)])
	created_at = models.DateTimeField(default=timezone.now, editable=False)

	def __unicode__(self):
		string = 'User ID: ' + str(self.user.id) + ' Roast ID: ' + str(self.roast.id) + ' Rating: ' + str(self.rating)
		return string

class RoastsOfTheDay(models.Model):
	roast_1 = models.OneToOneField(Roast, on_delete=models.CASCADE, related_name='roast_1')
	roast_2 = models.OneToOneField(Roast, on_delete=models.CASCADE, related_name='roast_2')
	roast_3 = models.OneToOneField(Roast, on_delete=models.CASCADE, related_name='roast_3')
	roast_4 = models.OneToOneField(Roast, on_delete=models.CASCADE, related_name='roast_4')
	roast_5 = models.OneToOneField(Roast, on_delete=models.CASCADE, related_name='roast_5')
	last_updated = models.DateTimeField(auto_now=True, editable=False)

class Alert(models.Model):
	ALERTS_TYPES = (
		('success', 'Success/Green'),
		('info', 'Info/Blue'),
		('warning', 'Warning/Yellow'),
		('danger', 'Danger/Red')
	)

	alert_type = models.CharField(max_length=7, choices=ALERTS_TYPES, default=ALERTS_TYPES[0][0], blank=False)

	message = models.TextField(blank=False)

	visible = models.BooleanField(default=False)