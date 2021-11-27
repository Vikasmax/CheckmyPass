import sys
import requests
import hashlib

def api_request_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f"error fetching: {res.status_code}, check the api ")
	return res  

def password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h,count in hashes:
		if h == hash_to_check:
			return count 
	return 0 	

def pwned_api_check(password):
	#checking if the password exits in API response
	sha1password = (hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
	first_5, tail =  sha1password[:5], sha1password[5:]
	response = api_request_data(first_5)
	return password_leaks_count(response, tail)


def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'{password} was found {count} times, you should change your password')
		else:
			print(f'{password} was NOT found, carry on ')

		return 'donnnnn'		



if __name__ == '__main__':
	main(sys.argv[1:])

