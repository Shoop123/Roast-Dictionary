from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import controller
from utils import make_int_list

def v1_search(request):
	return HttpResponse(controller.search(request.GET['key']))

def v1_main_search(request):
	return HttpResponse(controller.main_search(request.GET['key']))

def v1_update_rating(request):
	if request.user.is_authenticated():
		return HttpResponse(controller.update_rating(request.user, request.POST['id'], request.POST['rating']))
	else:
		raise PermissionDenied

def v1_edit_roast(request):
	if request.user.is_authenticated():
		return HttpResponse(controller.edit_roast(request.POST['roast_id'], request.POST['new_roast_body']))
	else:
		raise PermissionDenied

def v1_get_roast_ids(request):
	return HttpResponse(controller.get_roast_ids(request.GET['count']))

def v1_get_roast_rating(request):
	return HttpResponse(controller.get_roast_rating(request.GET['id']))

def v1_get_roast_by_id(request):
		return HttpResponse(controller.get_roast_by_id(request.GET['id']))

def v1_repopulate_db(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		return HttpResponse(controller.repopulate_db())
	else:
		raise PermissionDenied

def v1_delete_roast(request):
	if request.user.is_authenticated():
		controller.delete_roast(request.POST['roast_id'])
		return HttpResponse(status=200)
	else:
		raise PermissionDenied

def v1_get_keys(request):
	exclude_list = []

	result = make_int_list(request.GET['seen'])

	if result != -1:
		exclude_list = result

	focus_roast_id = None

	if 'focus-roast' in request.GET:
		focus_roast_id = int(request.GET['focus-roast'])

	return HttpResponse(controller.get_keys(request.user.username, request.user.id, exclude_list, focus_roast_id))

def v1_get_roasts_for_key(request):
	page = 1
	
	if 'page' in request.GET:
		page = int(request.GET['page'])

	key_name = request.GET['key_name']

	username = 'Anonymous'

	if request.user.is_authenticated():
		username = request.user.username

	return HttpResponse(controller.get_roasts_for_key(page, key_name, username))

def v1_get_roasts_for_user(request):
	username = request.GET['username']

	page = int(request.GET['page'])

	return HttpResponse(controller.get_roasts_for_user(username, request.user.username, page))