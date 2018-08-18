let keyPage = 2;

function loadMoreKeys() {

	let keyName = document.getElementsByClassName("key")[0].id;

	let url = GET_ROASTS_FOR_KEY + keyName + "&page=" + keyPage;

	let xmlHttp = new XMLHttpRequest();

	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4) {
			if(xmlHttp.status == 200) {
				
				addKeys(xmlHttp.responseText);
			} else {
				
				$('#btnLoadMore').fadeOut(250, function() {showNewKeys(jsonObj)});
			}
		}
	};

	xmlHttp.open(GET, url, true); // true for asynchronous 
	xmlHttp.send();
}

function addKeys(response) {

	if (response == null) return;

	let jsonObj = JSON.parse(response);

	updateKeyPage();

	if (jsonObj.end == true) {

		$('#btnLoadMore').fadeOut(250, function() {showMoreKeys(jsonObj)});
	} else {

		showMoreKeys(jsonObj);
	}
}

function showMoreKeys(jsonObj) {

	let roasts = jsonObj.roasts;

	let motherOfAllRoasts = document.getElementById("roasts");

	for (i = 0; i < roasts.length; i++) {
		
		let parentSpan = document.createElement("SPAN");
		parentSpan.className = "roast-info";

		let roastBody = document.createElement("FONT");
		roastBody.size = 4;
		roastBody.innerHTML = roasts[i].body;
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
		let valueText = document.createTextNode(roasts[i].rating);
		value.appendChild(valueText);

		let down = document.createElement("A");

		if ($("#main").data("info") == "logged_in") {

			up.className = "up-roast";
			up.id = "up-roast-" + roasts[i].id;

			down.className = "down-roast";
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

		let poster = document.createElement("FONT");
		poster.size = 2;
		poster.style.float = "right";

		if (roasts[i].user == "Anonymous") {

			poster.innerHTML = "Posted By: " + roasts[i].user;
		} else {

			poster.innerHTML = 'Posted By: <a href="/users/' + roasts[i].user_id + '">' + roasts[i].user + '</a>';
		}

		misc.appendChild(poster);
		misc.insertAdjacentHTML("beforeend", "<br>");

		if (roasts[i].keys.length > 0) {

			let otherKeysContainer = document.createElement("FONT");
			otherKeysContainer.size = 2;
			otherKeysContainer.innerHTML = "Other Keys: ";

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

		parentSpan.appendChild(misc);

		motherOfAllRoasts.appendChild(parentSpan);
	}
}

function updateKeyPage() {

	keyPage++;
}