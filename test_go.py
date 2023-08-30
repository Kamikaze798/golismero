import requests

urls = ['https://hack.me','hack.me:80','http://hack.me','hack.me:443','https://hack.me']

try:
	for url in urls:
		r = requests.get(url)
		print(f' the {url} is {r.status_code}')
except Exception as e:
	print(f'fail {url} {e}')