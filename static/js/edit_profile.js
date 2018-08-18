let email = document.getElementById('email');
let username = document.getElementById('username');
let btnSave = document.getElementById('save')

let startEmail = email.value;
let startUsername = username.value;

email.addEventListener('input', function()
{
    changeSaveButton();
});

username.addEventListener('input', function()
{
    changeSaveButton();
});

function changeSaveButton() {

	if (email.value != startEmail || username.value != startUsername) {

    	btnSave.disabled = false;
    } else {

    	btnSave.disabled = true;
    }
}