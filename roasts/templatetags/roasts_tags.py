from django import template
from roasts.models import Alert

register = template.Library()

ALERTS_TYPES = (
	'success',	# green
	'info',		# blue
	'warning',	# yellow
	'danger'	# red
)

@register.assignment_tag
def alerts():
	alert_context = {
		'show_alert': False,
		'alert_type': '',
		'alert_message': ''
	}

	if Alert.objects.exists():
		alert = Alert.objects.first()

		if alert.visible:
			alert_context['show_alert'] = True
			alert_context['alert_type'] = alert.alert_type
			alert_context['alert_message'] = alert.message

	return alert_context