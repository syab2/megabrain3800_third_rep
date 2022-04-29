import requests

res = requests.get('http://127.0.0.1:5000/api/games/1').json()

print(res)