let visible_home_ids = [];

function loadMoreHome() {

	let url = GET_KEYS + visible_home_ids;
	
	let xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				
				addHome(xmlHttp.responseText);
			} else {

				
				
				$('#btnLoadMore').fadeOut(250, function() {showNewKeys(jsonObj)});
			}
		}
	};

	xmlHttp.open(GET, url, true); // true for asynchronous 
	xmlHttp.send();
}

function addHome(response) {

	if (response == null) return;

	let jsonObj = JSON.parse(response);

	if (jsonObj.end == true) {

		let btnLoadMore = document.getElementById("btnLoadMore");

		$('#btnLoadMore').fadeOut(250, function() {showMoreHome(jsonObj)});
	} else {

		showMoreHome(jsonObj);
	}
}

function showMoreHome(jsonObj) {

	let keys = jsonObj.keys;

	for (i = 0; i < keys.length; i++) {
		saveHomeId(keys[i].id);

		$('#all-keys').append('<div class="key">\
									<span class="key-name">\
										<a href="/keys/' + keys[i].name + '/">\
											<h3 style="display: inline;">\
												<b><i>'+
													keys[i].name
												+'</i></b>\
											</h3>\
										</a>\
									</span>\
								<div class="roasts"></div></div>');

		for (j = 0; j < keys[i].roasts.length; j++) {

			var roast = keys[i].roasts[j];

			var upRoast = "";
			var downRoast = "";
			var postedBy = "";
			var displayOtherKeys = "";
			var otherKeys = "";
			var social = "";

			if ($('.main').data('info') == "logged_in") {
				if (roast.rated == 1) {
					upRoast = '<a class="up-roast active-roast" id="up-roast-'+roast.id+'" data-toggle="tooltip" data-placement="top" title="Uproast" rel="tooltip">\
									<i class="fa fa-angle-up"></i>\
								</a>';
					downRoast = '<a  class="down-roast disabled" id="down-roast-'+roast.id+'" data-toggle="tooltip" data-placement="bottom" title="Downroast" rel="tooltip">\
									<i class="fa fa-angle-down"></i>\
								</a>';
				} else if (roast.rated == 0) {
					upRoast = '<a class="up-roast" id="up-roast-'+roast.id+'" data-toggle="tooltip" data-placement="top" title="Uproast" rel="tooltip">\
									<i class="fa fa-angle-up"></i>\
								</a>';
					downRoast = '<a class="down-roast" id="down-roast-'+roast.id+'" data-toggle="tooltip" data-placement="bottom" title="Downroast" rel="tooltip">\
									<i class="fa fa-angle-down"></i>\
								</a>';
				} else {
					upRoast = '<a class="up-roast disabled" id="up-roast-'+roast.id+'" data-toggle="tooltip" data-placement="top" title="Uproast" rel="tooltip">\
									<i class="fa fa-angle-up"></i>\
								</a>';
					downRoast = '<a class="down-roast active-roast" id="down-roast-'+roast.id+'" data-toggle="tooltip" data-placement="bottom" title="Downroast" rel="tooltip">\
									<i class="fa fa-angle-down"></i>\
								</a>';
				}
			} else {
				upRoast = '<a data-toggle="modal" data-target="#logInModal" data-toggle="tooltip" data-placement="top" title="Uproast" rel="tooltip">\
								<i class="fa fa-angle-up"></i> \
							</a>';
				downRoast = '<a data-toggle="modal" data-target="#logInModal" data-toggle="tooltip" data-placement="bottom" title="Downroast" rel="tooltip">\
								<i class="fa fa-angle-down"></i>\
							</a>';
			}

			if (roast.user == "Anonymous") {
				postedBy = '<font size="2" style="float: right">\
								Posted By: Anonymous\
							</font>';
			} else {
				postedBy = '<font size="2" style="float: right">\
								Posted By: <a href="/users/' + roast.user_id + '">'+ roast.user + '</a>\
							</font>';
			}

			if (roast.otherKeys) {
				for(var k = 0; k < roast.otherKeys.length; k++) {
					otherKeys += '<a href="/keys/'+ roast.otherKeys[k] +'">'+ roast.otherKeys[k] +'</a>,';
				}
				otherKeys = otherKeys.slice(0, -1);
				displayOtherKeys = '<font size="2">Other Keys for this Roast: ' + otherKeys + '</font>';
			} 

			social = '<font size="2" style="float: right">\
						<a href="https://www.facebook.com/sharer/sharer.php?u=https://roastdictionary.com?focus-roast='+ roast.id +'" target="_blank">\
						  <i class="fa fa-facebook-official fa-lg" aria-hidden="true"></i>\
						</a>\
						&nbsp;\
						<a href="http://twitter.com/intent/tweet?text=Check+out+this+savage+roast&via=RoastDictionary&url=https://roastdictionary.com?focus-roast='+ roast.id +'&hashtags=roastdictionary" target="_blank">\
						  <i class="fa fa-twitter-square fa-lg" aria-hidden="true"></i>\
						</a>\
					</font>';

			$('.key').last().find(".roasts").append('\
				<span class="roast-info">\
					<font size="4">' +
						roast.roast
					+ '</font>'
					+ social +
					'<p>\
						<font size="2">\
							'+ upRoast +'\
							&nbsp;\
							<span id="roast-' + roast.id + '">' + roast.total + '</span>\
							'+ downRoast +'\
						</font>\
						'+ postedBy +'\
						'+ displayOtherKeys +'\
					</p>\
				</span>\
			');
		}
	}
}

function saveHomeId(id) {

	visible_home_ids.push(id);
}