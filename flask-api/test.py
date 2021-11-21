import requests

BASE = "http://127.0.0.1:5000/"

response = requests.patch(BASE + "video/3", {"name":"Harshit","views":909,"likes":111})
print(response.json())