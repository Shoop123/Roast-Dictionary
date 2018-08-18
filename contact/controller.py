from api.gmail_oauth import sauce_email

EMAIL = 'info@roastdictionary.com'

def send_email(from_email, subject, body, username):
	formatted_body = format_body(body, from_email, username)

	sauce_email(EMAIL, 'Contact: ' + subject, formatted_body)

def format_body(body, from_email, username):
	serperator = '-'*30
	info = '\n\n' + serperator + '\nEmail: ' + from_email + '\nUsername: ' + username
	body += info

	return body