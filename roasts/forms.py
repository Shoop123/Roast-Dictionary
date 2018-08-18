from django.forms import *
from models import Roast, Alert
from django.utils.translation import ugettext as _

class RoastForm(ModelForm):
	class Meta:
		model = Roast
		fields = ['body', 'keys']
		widgets = {
			'keys': SelectMultiple(attrs={'class': 'js-data-example-ajax-multiple', 'placeholder': 'Roast Description'}),
			'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'Roast Description'}),
		}

	def clean_keys(self):
		keys = self.cleaned_data['keys']

		if len(self.data['key_errors']) > 0:
			errors = []

			for error in self.data.getlist('key_errors'):
				errors.append(ValidationError(_(error), code='invalid key'))

			raise ValidationError(errors)

		return self.cleaned_data['keys']

	def clean_body(self):
		if self.data.getlist('roast_exists')[0] == 't':
			raise ValidationError(_('Roast already exists'), code='roast exists')

		return self.cleaned_data['body']