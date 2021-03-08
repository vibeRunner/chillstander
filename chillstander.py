# by viberunner
# simplistic password manager
# key best stored on a pendrive / SD card / CD/DVD disk...

# TODO: maybe add config file?
# - which type o' password preferred: totally random or words?
# - where database and where key?
# - set if you'd rather have the password printed or copied to clipboard

# TODO: add PIN for extra security measure

# TODO: make list_websites() neater

import json
from cryptography.fernet import Fernet
from datetime import datetime
import faker
f = faker.Faker()


def get_key():
	
	key_location = '/Volumes/T7/files/private/memories/key.txt'

	try:

		key_file = open(key_location, 'r')
		key = str.encode(key_file.read())
		key_file.close()

	except:

		try:
			input('\nMISSING KEY.\nGenerate a new key and/or edit the key path.\nPRESS [ENTER] TO QUIT.')
		except:
			pass

		exit(1)


	return Fernet(key)


def generate_key():

	file = open('key.txt', 'w')
	file.write( Fernet.generate_key().decode("utf-8") )
	file.close()

	print('\nRemember to move key.txt to a seperate data drive!')
	print('Make sure to remove key from this folder afterwards!')
	print('Update file path in the script!\n')

	try:
		input('Press [ENTER] when you read this.')
	except:
		pass


def get_password_dict(f):
	

	passwd_file = open('.passwds.enc', 'r')
	out = json.loads( f.decrypt( str.encode(passwd_file.read() ) ) )
	
	passwd_file.close()
	return out


def write_to_passwords(f):
	
	website = input('\n> Website: ')
	username = input('> Username: ')
	password = input('> Password: ')	

	try:
		out = get_password_dict(f)   # when file has something 
	except:
		out = {}                     # when file empty

	out.update({website:{'username':username, 'password':password}})
	
	file = open('.passwds.enc', 'w')
	file.write( f.encrypt( str.encode( json.dumps(out) ) ).decode("utf-8") )
	file.close()


def list_websites(f):

	print()
	database = get_password_dict(f)
	print("WEBSITE : USERNAME")
	for site in database:
		print(f"{site} : {database[site]['username']}")
	# TODO: make it look like a chart, according to length spaces are added...


def remove_entry(f, entry):
	try:
		out = get_password_dict(f)
	except:
		print('No pre-existing password file.')
		pass

	try:
		out.pop(entry)
		file = open('.passwds.enc', 'w')
		file.write( f.encrypt( str.encode( json.dumps(out) ) ).decode("utf-8") )
		file.close()
	except:
		print('No such entry.')
		pass

def get_entry(f, site):

	database = get_password_dict(f)
	print(f"\n{database[site]['username']} : {database[site]['password']}")


def elegant_exit():

	hour = int(datetime.now().strftime("%H"))

	if hour >= 4 and hour <= 19:
		exit("\nHave a nice day.\n")

	elif hour > 20:
		exit("\nHave a productive night.\n")


def generate_overrated_password():
	return f.password(12)


def generate_elegant_password(w_count):

	out = ""
	for i in range(w_count):
		out += f.word()
	return out


### -----------------


print('\n------------ by viberunner ------------')
print('----- chillstander.py version 1.0 -----')

while True:

	command = input('\n> ').lower()

	if command == 'help' or command == 'h':
		print("\nkeygen\nget [website]\nrm [website]\nlist\nadd\ngen\nexit")

	elif command == "list":
		list_websites( get_key() )

	elif command.split(' ')[0] == "get":
		get_entry( get_key(), command.split(' ')[1] )

	elif command == "add":
		write_to_passwords( get_key() )

	elif command == "keygen":
		generate_key()

	elif command == "gen":
		print(f"\n{generate_elegant_password(4)}")
		#print(f"\n{generate_overrated_password()}")

	elif command.split(' ')[0] == "rm":
		remove_entry( get_key(), command.split(' ')[1])

	elif command == "exit":
		elegant_exit()

	else:
		print('\nUnknown command. When in doubt, type "help".')
