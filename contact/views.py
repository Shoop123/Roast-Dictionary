from django.shortcuts import render, redirect

import forms

import controller

THANK_YOU = '../thank_you'

def contact(request):
	initial_state = {}
	if request.user.is_authenticated():
		initial_state['email'] = request.user.email

	form = forms.ContactForm(request.POST or None, initial=initial_state)

	if form.is_valid():
		controller.send_email(form.cleaned_data['email'], form.cleaned_data['subject'], form.cleaned_data['body'], request.user.username)
		return redirect(THANK_YOU)

	context = {
		'form': form
	}

	return render(request, 'contact/contact.html', context)

def thank_you(request):
	return render(request, 'contact/thank_you.html')