let profilePage = 2;

function loadMoreProfile() {

	let username = $('#username').data('info');

	let url = GET_ROASTS_FOR_PROFILE + username + "&page=" + profilePage;

	let xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				
				addProfile(xmlHttp.responseText);
			} else {

				console.log('error on profile');

				$('#btnLoadMore').fadeOut(250, function() {showNewKeys(jsonObj)});
			}
		}
	};

	xmlHttp.open(GET, url, true); // true for asynchronous 
	xmlHttp.send();
}

function addProfile(response) {

	if (response == null) return;

	let jsonObj = JSON.parse(response);

	updateProfilePage();

	if (jsonObj.end == true) {
		console.log('about to show');

		$('#btnLoadMore').fadeOut(250, function() {showMoreProfile(jsonObj)});
	} else {

		showMoreProfile(jsonObj);
	}
}

function showMoreProfile(jsonObj) {

	let roasts = jsonObj.roasts;

	if (roasts == undefined) {

		return;
	}

	let motherOfAllRoasts = document.getElementById("all-roasts");

	for (i = 0; i < roasts.length; i++) {
		
		let parentSpan = document.createElement("SPAN");
		parentSpan.className = "roast-info";
		parentSpan.id = roasts[i].id

		let roastBody = document.createElement("FONT");
		roastBody.size = 4;
		roastBody.innerHTML = roasts[i].roast;
		parentSpan.appendChild(roastBody);

		let social = document.createElement("FONT");
		social.size = 2;
		social.innerHTML = '<font size="2" style="float: right">\
						<a href="https://www.facebook.com/sharer/sharer.php?u=https://roastdictionary.com?focus-roast='+ roasts[i].id +'" target="_blank">\
						  <i class="fa fa-facebook-official fa-lg" aria-hidden="true"></i>\
						</a>\
						&nbsp;\
						<a href="http://twitter.com/intent/tweet?text=Check+out+this+savage+roast&via=RoastDictionary&url=https://roastdictionary.com?focus-roast='+ roasts[i].id +'&hashtags=roastdictionary" target="_blank">\
						  <i class="fa fa-twitter-square fa-lg" aria-hidden="true"></i>\
						</a>\
					</font>';
		parentSpan.appendChild(social);

		let misc = document.createElement("P");

		let ratingsParent = document.createElement('FONT');
		ratingsParent.size = 2;

		let up = document.createElement("A");

		let value = document.createElement("SPAN");
		value.setAttribute("id", "roast-"+roasts[i].id);
		let valueText = document.createTextNode(roasts[i].total);
		value.appendChild(valueText);

		let down = document.createElement("A");

		if ($("#main").data("info") == "logged_in") {

			if (roasts[i].rated == 1) {

				up.className = "up-roast active-roast";
				down.className = "down-roast disabled";

			} else if (roasts[i].rated == -1) {

				up.className = "up-roast disabled";
				down.className = "down-roast active-roast";
			} else {

				up.className = "up-roast";
				down.className = "down-roast";
			}
			
			up.id = "up-roast-" + roasts[i].id;			
			down.id = "down-roast-" + roasts[i].id;

		} else {

			up.setAttribute("data-toggle", "modal");
			up.setAttribute("data-target", "#logInModal");

			down.setAttribute("data-toggle", "modal");
			down.setAttribute("data-target", "#logInModal");
		}

		up.setAttribute("data-toggle", "tooltip");
		up.setAttribute("data-placement", "top");
		up.setAttribute("title", "Uproast");
		up.setAttribute("rel", "tooltip");
		down.setAttribute("data-toggle", "tooltip");
		down.setAttribute("data-placement", "bottom");
		down.setAttribute("title", "Downroast");
		down.setAttribute("rel", "tooltip");

		let totalRating = document.createElement("SPAN");
		totalRating.id = "roast-" + roasts[i].id;
		totalRating.innerHTML = roasts[i].total;

		let upArrow = document.createElement("I");
		upArrow.className = "fa fa-angle-up";
		up.appendChild(upArrow);
		let downArrow = document.createElement("I");
		downArrow.className = "fa fa-angle-down";
		down.appendChild(downArrow);

		ratingsParent.appendChild(up);
		ratingsParent.insertAdjacentHTML("beforeend", "&nbsp;");
		ratingsParent.appendChild(value);
		ratingsParent.appendChild(down);

		misc.appendChild(ratingsParent);
		misc.insertAdjacentHTML("beforeend", "&nbsp;");

		if ($("#main").data("info") == "not_logged_in") {

			let poster = document.createElement("FONT");
			poster.size = 2;
			poster.style.float = "right";
			poster.innerHTML = "Posted By: " + roasts[i].user;

			misc.appendChild(poster);
		}

		misc.insertAdjacentHTML("beforeend", "<br>");

		if (roasts[i].keys.length > 0) {

			let otherKeysContainer = document.createElement("FONT");
			otherKeysContainer.size = 2;
			otherKeysContainer.innerHTML = "Keys: ";

			for (j = 0; j < roasts[i].keys.length; j++) {

				let keyLink = document.createElement("A");
				keyLink.href = "/keys/" + roasts[i].keys[j];
				keyLink.innerHTML = roasts[i].keys[j];

				otherKeysContainer.appendChild(keyLink);

				if (j < roasts[i].keys.length - 1) {

					otherKeysContainer.innerHTML += ", ";
				}
			}

			misc.appendChild(otherKeysContainer);
		}

		if ($("#main").data("info") == "logged_in" && $("#current-user-username").data("info") == roasts[i].user) {

			misc.insertAdjacentHTML("beforeend", "<br>");

			let editLink = document.createElement("A");
			editLink.type = "button";
			editLink.href = "/edit_roast/?roast_id=" + roasts[i].id;
			editLink.className = "btn btn-primary";
			editLink.innerHTML = "Edit";

			let deleteButton = document.createElement("INPUT");
			deleteButton.type = "button";
			deleteButton.className = "btn btn-danger";
			deleteButton.value = "Delete";
			deleteButton.onclick = new Function("deleteRoast('" + roasts[i].id + "')");

			let alertMessage = document.createElement("DIV");
			alertMessage.id = "alert-" + roasts[i].id;
			alertMessage.className = "alert alert-danger alert-dismissible hide";
			alertMessage.role = "alert";

			let closeAlertButton = document.createElement("BUTTON");
			closeAlertButton.type = "button";
			closeAlertButton.className = "close";
			closeAlertButton.setAttribute("aria-label", "Close");
			closeAlertButton.setAttribute("onclick", "closeAlert('alert-'+" + roasts[i].id + ")");

			let closeAlertButtonSpan = document.createElement("SPAN");
			closeAlertButtonSpan.setAttribute("aria-hidden", "true");
			closeAlertButtonSpan.innerHTML = "&times;";

			closeAlertButton.appendChild(closeAlertButtonSpan);

			alertMessage.appendChild(closeAlertButton);

			alertMessage.innerHTML += "Error deleting roast";

			misc.appendChild(editLink);
			misc.insertAdjacentHTML("beforeend", "&nbsp;");
			misc.appendChild(deleteButton);
			parentSpan.appendChild(misc);
			parentSpan.appendChild(alertMessage);
		} else {

			parentSpan.appendChild(misc);
		}

		motherOfAllRoasts.appendChild(parentSpan);
	}
}

function updateProfilePage() {

	profilePage++;
}