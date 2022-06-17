from fileinput import filename
import json
import requests
from jsonschema import validate

def get_only(url, schema): 
    #requests.get to do a GET request to the given api
    response = requests.get(url)
    print(response.json())
    with open(schema, "r") as f:
        validate(response.json(), json.load(f))

def get_check(url, schema, pong):
    api_url = url + "/" + pong
    #requests.get to do a GET request to the given api
    response = requests.get(api_url)
    print(response.json())
    with open(schema, "r") as f:
        validate(response.json(), json.load(f))
    if response.json()['response']['body']['pong'] == pong:
        print("Correct")
    else:
        print("Error")

if __name__ == '__main__':
    get_only()
    get_check()