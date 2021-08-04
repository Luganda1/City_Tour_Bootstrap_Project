import requests
import os
import pprint

ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
SECRET_KEY = os.environ.get("UNSPLASH_SECRETE_KEY")

endpoint = "https://api.unsplash.com/"
endpoint1= f"https://api.unsplash.com/photos/?client_id={ACCESS_KEY}"
headers = {
    "client_id": ACCESS_KEY
}
response = requests.get(url=endpoint1)
response.raise_for_status()

data = response.json()

print(data)







