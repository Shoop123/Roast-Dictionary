from django.contrib import admin

# Register your models here.

from .models import Key, Roast, Rating, Alert

class AlertAdmin(admin.ModelAdmin):
	list_display = ('alert_type', 'message', 'visible')

	def save_model(self, request, obj, form, change):
		alerts = Alert.objects.all()

		if alerts.exists():
			alerts.delete()

		obj.save()

	class Meta:
		model = Alert

admin.site.register(Key)
admin.site.register(Roast)
admin.site.register(Rating)
admin.site.register(Alert, AlertAdmin)