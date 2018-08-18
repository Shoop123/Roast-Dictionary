
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'gmail-python-email-send.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:

		# try:
		# 	import argparse
		# 	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		# except ImportError:
		# 	flags = None

		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store, flags)
		print('Storing credentials to ' + credential_path)
	return credentials

def send_message(service, user_id, message):
	"""Send an email message.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	message: Message to be sent.

	Returns:
	Sent Message.
	"""
	try:
		message = (service.users().messages().send(userId=user_id, body=message)
				   .execute())
		print 'Message Id: %s' % message['id']
		return message
	except Exception as err:
		print 'An error occurred: %s' % err

def create_message(sender, to, subject, message_text):
	from email.mime.text import MIMEText
	import base64
	"""Create a message for an email.

	Args:
	sender: Email address of the sender.
	to: Email address of the receiver.
	subject: The subject of the email message.
	message_text: The text of the email message.

	Returns:
	An object containing a base64url encoded email object.
	"""

	# Make sure email addresses do not contain non-ASCII characters
	sender = sender.encode('ascii')
	to = to.encode('ascii')

	for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
		try:
			message_text.encode(body_charset)
		except UnicodeError:
			pass
		else:
			break

	message = MIMEText(message_text.encode(body_charset), 'plain', body_charset)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.urlsafe_b64encode(message.as_string())}

ROAST_DICTIONARY_EMAIL = 'info@roastdictionary.com'

def sauce_email(to_email, subject, body):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	message = create_message(ROAST_DICTIONARY_EMAIL, to_email, subject, body)
	send_message(service, ROAST_DICTIONARY_EMAIL, message)

def sauce_emails(email_list, subject_list, body_list):
	assert len(email_list) == len(subject_list) == len(body_list), 'All 3 lists must have the same length'

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	length = len(email_list)

	messages = []

	for i in range(len(length)):
		messages.append(create_message(ROAST_DICTIONARY_EMAIL, email_list[i], subject_list[i], body_list[i]))

	for i in range(len(length)):
		send_message(service, ROAST_DICTIONARY_EMAIL, messages[i])