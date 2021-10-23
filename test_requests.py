import requests

r = requests.get('https://howrare.is/')

print(r.text)