from functools import reduce
from operator import add
from itertools import izip
import string
from roasts.models import Key, Roast

VALID_CHARS = '_+-'

def textToNumber(text):
	list(text)
	numbers = []
	for x in text:

		num = ord(x)
		if len(str(num)) == 2:
			numbers.append( str(ord(x)) + "0")
		else:
			numbers.append(str(ord(x)))
	return "".join(numbers)


def numberToText(number):
	x = iter(str(number))
	numbers = [reduce(add, tup) for tup in izip(x, x, x)]
	letters = []

	for y in numbers:
		if int(y) > 300:
			letters.append(chr(int(y[0:2])))
		else:
			letters.append(chr(int(y)))
			
	return "".join(letters)

def is_valid_key(key):
	try:
		key = key.decode('ascii')
	except UnicodeDecodeError:
		return False
	except:
		return False

	invalidChars = string.punctuation

	for c in VALID_CHARS:
		invalidChars = invalidChars.replace(c, '')

	invalidChars = set(invalidChars)
	
	if key.strip() == '' or any(char in invalidChars for char in key) or key.isdigit():
		return False

	return True

def create_valid_keys(keys):
	ids = []
	invalid_keys = []

	for key in keys:
		key_str = str(key).strip()

		if key_str.isdigit():
			key_id = int(key_str)

			if Key.objects.filter(id=key_id).exists():
				ids.append(key_id)
			else:
				invalid_keys.append(key)
		elif not is_valid_key(key_str):
			invalid_keys.append(key_str)
		else:
			new_key = Key(name=key_str)
			new_key.save()
			ids.append(new_key.id)

	invalid_keys = list(set(invalid_keys))

	if len(invalid_keys) > 0:
		errors = []

		for invalid_key in invalid_keys:
			errors.append('"{}" is an invalid key'.format(invalid_key))

		return False, ids, errors

	return True, ids, []

def valid_roast(roast, key_ids):
	roast = roast.strip()
	roasts = Roast.objects.filter(body=roast)

	if roasts.exists():
		match = True

		for key_id in key_ids:
			if not Roast.objects.filter(body=roast, keys=key_id).exists():
				match = False
				break

		if match:
			return False, []

		roast = Roast.objects.get(body=roast)

		added_keys = []

		for id in key_ids:
			if not Roast.objects.filter(body=roast, keys=id).exists():
				key = Key.objects.get(id=id)
				roast.keys.add(Key.objects.get(id=id))
				added_keys.append(id)

		return False, added_keys
	else:
		return True, []

def make_int_list(csv_str):
	split = csv_str.split(',')

	int_list = []

	for num in split:
		if num.strip().isdigit():
			int_list.append(int(num.strip()))
		else:
			return -1

	return int_list