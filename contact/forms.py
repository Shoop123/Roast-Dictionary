from django import forms

class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'id' : "email", 'type' : "email", 'class': "form-control", 'placeholder': "Email"}))
	subject = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'id' : "subject", 'type' : "text", 'class': "form-control", 'placeholder': "Subject"}))
	body = forms.CharField(widget=forms.Textarea(attrs={'id' : "body", 'class': 'form-control', 'placeholder': 'Body'}))