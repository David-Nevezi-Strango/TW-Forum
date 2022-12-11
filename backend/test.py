#test script to verify the functionality of the api
import requests

base = "http://127.0.0.1:5000/"

response = requests.put(base + "comment/6" , {"text":"ey"})
print(response)
response = requests.get(base + "comment/6")
print(response.json())