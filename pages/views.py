from django.shortcuts import render

# import controller

def about(request):
	return render(request, 'pages/about.html')

def terms(request):
	return render(request, 'pages/terms.html')

def privacy(request):
	return render(request, 'pages/privacy.html')