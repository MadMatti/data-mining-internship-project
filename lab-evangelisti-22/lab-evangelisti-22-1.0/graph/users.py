import requests
import json
from jsonschema import validate
import sys

def list_users(token):
    endpoint = "https://graph.microsoft.com/v1.0/users?$top=999&$select=id,givenName"
    headers = {'Authorization': 'Bearer ' + token}
    users = requests.get(endpoint, headers=headers).json()
    return users['value']

def validate_all(response, file_schema):
    users = response
    with open(file_schema, "r") as f:
        schema = json.load(f)
    for user in users:
        try:
            validate(user, schema)
        except Exception as err:
            sys.exit("Error: " + str(err))

def insert_users(conn, users, file_schema):
    validate_all(users, file_schema)
    cur = conn.cursor()
    for user in users:
        id = user['id']
        name = user['givenName']
        sql_check = '''select exists(select user_id from public.users where user_id=(%s))'''
        sql_insert = '''INSERT INTO public.users (user_id, givenname)
                        VALUES (%s, %s)'''
        cur.execute(sql_check, (id,))
        if cur.fetchone()[0] is False:
            cur.execute(sql_insert, (id, name))
    conn.commit()
    cur.close()
    print("Users have been added to the database")


