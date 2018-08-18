from django.conf.urls import url

from .views import (
	v1_search,
	v1_main_search,
	v1_update_rating,
	v1_get_roast_ids,
	v1_get_roast_rating,
	v1_get_roast_by_id,
	v1_get_roasts_for_key,
	v1_get_roasts_for_user,
	v1_repopulate_db,
	v1_get_keys,
	v1_edit_roast,
	v1_delete_roast
)

urlpatterns = [
	url(r'^v1/search/$', v1_search),
	url(r'^v1/main_search/$', v1_main_search),
	url(r'^v1/update_rating/$', v1_update_rating),
	url(r'^v1/get_roast_ids/$', v1_get_roast_ids),
	url(r'^v1/get_roast_rating/$', v1_get_roast_rating),
	url(r'^v1/get_roast_by_id/$', v1_get_roast_by_id),
	url(r'^v1/get_roasts_for_key/$', v1_get_roasts_for_key),
	url(r'^v1/get_roasts_for_user/$', v1_get_roasts_for_user),
	url(r'^v1/repopulate_db/$', v1_repopulate_db),
	url(r'^v1/get_keys/$', v1_get_keys),
	url(r'^v1/edit_roast/$', v1_edit_roast),
	url(r'^v1/delete_roast/$', v1_delete_roast)
]