$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip()

	$('body').tooltip({
	    selector: '[rel=tooltip]'
	});

  $('body').delegate('.up-roast', 'click', function() {
	// console.log(this)
	var uproast = this.id;
	var id = parseInt(uproast.replace("up-roast-", ""));
	var user_id = $('.profile-id').data("profile-id");

	console.log('user_id ' + user_id);

	$.ajax({
			type: POST,
			url: "/api/v1/update_rating/",
			data: {
				'id': id,
				'rating': 1,
				'user_id': user_id, 
				"csrfmiddlewaretoken": getCookie("csrftoken")
			},
			success: function(response) {
			  // if (rating > 0) {
		   //      $('#roast-' + id).html(parseInt($('#roast-' + id).html()) + 1)
		   //    } else {
		   //      $('#roast-' + id).html(parseInt($('#roast-' + id).html()) - 1)
		   //    }
				console.log('success');
				console.log(response);

				response = JSON.parse(response);

				var difference = Math.abs(parseInt($('#roast-' + id).html()) - response.total);

				if (difference > 1) {
					console.log("TESTING");
					$('[id=up-roast-' + id + ']').toggleClass('active-roast');
					$('[id=down-roast-' + id + ']').toggleClass('active-roast');
				} else {
					console.log("TESTING");
					$('[id=up-roast-' + id + ']').toggleClass('active-roast');
					$('[id=down-roast-' + id + ']').toggleClass('disabled');
				}

				
				console.log($('#roast-' + id));
				console.log(response);
				$('[id=roast-'+id+']').html(response.total);
			},
			error: function() {
				alert('Error');
			}
		});
  })


  $('body').delegate('.down-roast', 'click', function() {
	console.log(this)
	var downroast = this.id;
	var id = parseInt(downroast.replace("down-roast-", ""));
	var user_id = $('.profile-id').data("profile-id");

	console.log('user_id ' + user_id);

	$.ajax({
		type: POST,
		url: "/api/v1/update_rating/",
		data: {
			'id': id,
			'rating': -1,
			'user_id': user_id, 
			"csrfmiddlewaretoken": getCookie("csrftoken")
		},
		success: function(response) {
		  // if (rating > 0) {
	   //      $('#roast-' + id).html(parseInt($('#roast-' + id).html()) + 1)
	   //    } else {
	   //      $('#roast-' + id).html(parseInt($('#roast-' + id).html()) - 1)
	   //    }
			console.log('success');
			console.log(response);

			response = JSON.parse(response);

			var difference = Math.abs(parseInt($('#roast-' + id).html()) - response.total);

			if (difference > 1) {
				$('[id=up-roast-' + id + ']').toggleClass('active-roast');
				$('[id=down-roast-' + id + ']').toggleClass('active-roast');
			} else {
				$('[id=up-roast-' + id + ']').toggleClass('disabled');
				$('[id=down-roast-' + id + ']').toggleClass('active-roast');
			}

			$('[id=roast-' + id + ']').html(response.total);
		},
		error: function() {
			alert('Error');
		}
	});
  })

  // $('.down-roast').click(function() {
  //   var downroast = this.id;
  //   var id = downroast.replace("down-roast-", "");
  //   $(this).toggleClass('active');
  //   $('#up-roast-' + id).toggleClass('disabled');
  //   if ( $('#down-roast-' + id + '.active').length > 0 ) {
  //     updateRating(parseInt(id), -1);
  //   } else {
  //     updateRating(parseInt(id), 1);
  //   }
  // })


	function formatRepo (repo) {
			if (repo.loading) return repo.text;

			var markup = "<div class='select2-result-repository clearfix'>" +
				"<div class='select2-result-repository__avatar'><img src='" + repo.owner.avatar_url + "' /></div>" +
				"<div class='select2-result-repository__meta'>" +
					"<div class='select2-result-repository__title'>" + repo.full_name + "</div>";

			if (repo.description) {
				markup += "<div class='select2-result-repository__description'>" + repo.description + "</div>";
			}

			markup += "<div class='select2-result-repository__statistics'>" +
				"<div class='select2-result-repository__forks'><i class='fa fa-flash'></i> " + repo.forks_count + " Forks</div>" +
				"<div class='select2-result-repository__stargazers'><i class='fa fa-star'></i> " + repo.stargazers_count + " Stars</div>" +
				"<div class='select2-result-repository__watchers'><i class='fa fa-eye'></i> " + repo.watchers_count + " Watchers</div>" +
			"</div>" +
			"</div></div>";

			return markup;
		}

		function formatRepoSelection (repo) {
			return repo.full_name || repo.text;
		}


	$(".js-example-data-ajax").select2({
	  width: '100%',
	  placeholder: "Search Keywords",
	  ajax: {
		url: MAIN_SEARCH,
		dataType: 'json',
		delay: 250,
		data: function (params) {
		  return {
			key: params.term, // search term
			page: params.page
		  };
		},
		processResults: function (data, params) {
		  // parse the results into the format expected by Select2
		  // since we are using custom formatting functions we do not need to
		  // alter the remote JSON data, except to indicate that infinite
		  // scrolling can be used
		  params.page = params.page || 1;

		  return {
			results: data.keys,
			pagination: {
			  more: (params.page * 30) < data.total_count
			}
		  };
		},
		cache: true
	  },
	  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
	  minimumInputLength: 1,
	  templateResult: formatRepoOther, // omitted for brevity, see the source of this page
	  templateSelection: formatRepoSelectionOther // omitted for brevity, see the source of this page
	});



	function formatRepoOther (key) {
	  return key.name
	}


	function formatRepoSelectionOther (key) {
	  window.open(KEY_ROOT + key.name ,"_self");
	  if (key.name == "Add new keyword") {
		return key.new_value;
	  }else {
		return key.text;
	  }
	}



	$(".js-data-example-ajax-multiple").select2({
	  width: '100%',
	  placeholder: "Search Keywords",
	  ajax: {
		url: SEARCH,
		dataType: 'json',
		delay: 250,
		data: function (params) {
		  return {
			key: params.term, // search term
			page: params.page
		  };
		},
		processResults: function (data, params) {
		  // parse the results into the format expected by Select2
		  // since we are using custom formatting functions we do not need to
		  // alter the remote JSON data, except to indicate that infinite
		  // scrolling can be used
		  params.page = params.page || 1;

		  return {
			results: data.keys,
			pagination: {
			  more: (params.page * 30) < data.total_count
			}
		  };
		},
		cache: true
	  },
	  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
	  minimumInputLength: 1,
	  templateResult: formatKey, // omitted for brevity, see the source of this page
	  templateSelection: formatKeySelection // omitted for brevity, see the source of this page

	});

	function formatKey (key) {
			return key.name
		}


  function formatKeySelection (key) {
	console.log(key);

		if (key.name == "Add new keyword") {
			return key.new_value;
		}else {
			return key.text;
		}
		
  }

});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
				
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	
	return cookieValue;
}


function updateRating(id, rating, action) {

	$.ajax({
		type: POST,
		url: "/api/v1/update_rating/",
		data: {
			'id': id,
			'rating': rating,
			"csrfmiddlewaretoken": getCookie("csrftoken")
		},
		success: function() {
		  if (rating > 0) {
			$('#roast-' + id).html(parseInt($('#roast-' + id).html()) + 1)
		  } else {
			$('#roast-' + id).html(parseInt($('#roast-' + id).html()) - 1)
		  }
		},
		error: function() {
			alert('Error');
		}
	});
}

function deleteRoast(roastID) {
	let url = DELETE_ROAST;
	
	let data = {
		"roast_id": roastID
	};

	post(url, data, removeRoast, showError, roastID, roastID);
}

function removeRoast(roastID) {

	var span = document.getElementById(roastID);
	span.parentNode.removeChild(span);
}

function showError(roastID) {

	let a = document.getElementById('alert-' + roastID);
	a.classList.remove('hide');
	a.classList.add('show');
}

function closeAlert(alertID) {

	let a = document.getElementById(alertID);
	a.classList.remove('show');
	a.classList.add('hide');
}

function post(url, data, success, error, successParams, errorParams) {

	data["csrfmiddlewaretoken"] = getCookie("csrftoken");

	$.ajax({
		type: POST,
		url: url,
		data: data,

		success: function() {

			if (success != null) {
				
				success(successParams);
			}
		},
		error: function() {

			if (error != null) {

				error(errorParams);
			}
		}
	});
}

function toggleUp(id) {
  if ( $('#disabled-roast-' + id).length > 0 ) {

  } else {

  }
}


