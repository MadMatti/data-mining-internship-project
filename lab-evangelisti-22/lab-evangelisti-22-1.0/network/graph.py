import requests
import json

if __name__ == "__main__":
    api = "https://graph.microsoft.com/v1.0/me"
    #par = {'id': '00278b73-459c-4907-9e5b-11537a5fbb74', 
    #       'userPrincipalName': "m.evangelisti@ubroker.it"}
    token = ""
    auth = {'Authorization': 'Bearer ' + token}
    req = requests.get(url = api, headers = auth)
    data = req.json()
    print("User: " + data['userPrincipalName'] + "\n")
    print(json.dumps(data, indent=4))
