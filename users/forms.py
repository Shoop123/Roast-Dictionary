from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.forms import PasswordResetForm, loader, EmailMultiAlternatives

from django.utils.translation import ugettext as _

from api.gmail_oauth import sauce_email

USERNAME_MAX_LENGTH = 40
PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 5

PASSWORD_TOO_SHORT_ERROR = 'Password must be at least {} characters long'.format(PASSWORD_MIN_LENGTH)

class SignUpForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'id' : "email", 'type' : "email", 'class': "form-control", 'placeholder': "Email"}))
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH, widget=forms.TextInput(attrs={'id' : "username", 'type' : "text", 'class': "form-control", 'placeholder': "Username"}))
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.TextInput(attrs={'id' : "password", 'type' : "password", 'class': "form-control", 'placeholder': "Password"}))

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(_("Username is already taken"), code='username taken')

		return username

	def clean_password(self):
		password = self.cleaned_data.get('password')

		if len(password) < PASSWORD_MIN_LENGTH:
			raise forms.ValidationError(_(PASSWORD_TOO_SHORT_ERROR), code='password too short')

		return password

class LoginForm(forms.Form):
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Username"}))
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Password"}))
	
	def clean(self):
		clean_username = self.cleaned_data.get('username')
		clean_password = self.cleaned_data.get('password')

		if clean_username and clean_password:
			user = authenticate(username=clean_username, password=clean_password)

			if user is None:
				raise forms.ValidationError(_("Username or password is incorrect. Note that both fields are case-sensitive."), code='invalid')

		return self.cleaned_data

class CustomPasswordResetForm(PasswordResetForm):
	def clean_email(self):
		email = self.cleaned_data.get('email')

		if not User.objects.filter(email=email).exists():
			raise forms.ValidationError(_("Email not found"), code='email not found')

		return email

	def send_mail(self, subject_template_name, email_template_name,
				  context, from_email, to_email, html_email_template_name=None):
		"""
		Send a django.core.mail.EmailMultiAlternatives to `to_email`.
		"""

		subject = loader.render_to_string(subject_template_name, context)
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())
		body = loader.render_to_string(email_template_name, context)

		sauce_email(to_email, subject, body)

class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput(attrs={'type' : "password", 'class': "form-control", 'placeholder': "Old Password"}))
	new_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput(attrs={'type' : "password", 'class': "form-control", 'placeholder': "New Password"}))
	verify_new_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput(attrs={'type' : "password", 'class': "form-control", 'placeholder': "New Password Again"}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordChangeForm, self).__init__(*args, **kwargs)

	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password')

		if not self.user.check_password(old_password):
			raise forms.ValidationError(_("Incorrect password"), code='incorrect password')

		return old_password

	def clean_new_password(self):
		new_password = self.cleaned_data.get('new_password')

		if len(new_password) < PASSWORD_MIN_LENGTH:
			raise forms.ValidationError(_(PASSWORD_TOO_SHORT_ERROR), code='new password is too short')

		return new_password

	def clean_verify_new_password(self):
		verify_new_password = self.cleaned_data.get('verify_new_password')
		new_password = self.cleaned_data.get('new_password')

		if verify_new_password != new_password:
			raise forms.ValidationError(_("Passwords don't match"), code='passwords don\'t match')

		return verify_new_password

class AccountForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'id' : "username", 'type' : "text", 'class': "form-control", 'placeholder': "Username"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'id' : "email", 'type' : "email", 'class': "form-control", 'placeholder': "Email"}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AccountForm, self).__init__(*args, **kwargs)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		
		if self.user.username != username:
			if User.objects.filter(username=username).exists():
				raise forms.ValidationError(_("Username is already in use"), code='username taken')

		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		
		if self.user.email != email:
			if User.objects.filter(email=email).exists():
				raise forms.ValidationError(_("Email is already in use"), code='email taken')

		return email