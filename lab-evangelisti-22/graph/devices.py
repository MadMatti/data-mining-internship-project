import requests
import json
from jsonschema import validate
import sys
from datetime import datetime, timedelta

def list_devices(token):
    endpoint = "https://graph.microsoft.com/v1.0/devices?$top=999&$select=deviceID,id,displayName,registrationDateTime,approximateLastSignInDateTime"
    headers = {'Authorization': 'Bearer ' + token}
    devices = requests.get(endpoint, headers=headers).json()
    return devices['value']

def validate_all(response, file_schema):
    devices = response
    with open(file_schema, "r") as f:
        schema = json.load(f)
    for device in devices:
        try:
            validate(device, schema)
            if device['registrationDateTime'] is not None:
                try:
                    create_date_obj(device['registrationDateTime'])
                except Exception as err:
                    sys.exit("Error " + str(err))
        except Exception as err:
            sys.exit("Error: " + str(err))

def create_date_obj(dateString):
    if dateString is None: return None
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    date_obj = datetime.strptime(dateString, date_format)
    return date_obj

def list_active_devices(devices, active_period):
    today = datetime.now()
    start_date = (today - timedelta(days=active_period, hours=today.hour, minutes=today.minute, seconds=today.second)).strftime("%Y-%m-%dT%H:%M:%SZ")
    active_devices = []
    for device in devices:
        last_login = device['approximateLastSignInDateTime']
        if last_login is not None and last_login >= start_date:
            active_devices.append(device)
    return active_devices

def delete_devices(cur, active_period):
    today = datetime.now()
    start_date = (today - timedelta(days=active_period, hours=today.hour, minutes=today.minute, seconds=today.second)).strftime("%Y-%m-%dT%H:%M:%SZ")
    start_obj = create_date_obj(start_date)
    sql_delete = '''delete from public.devices where last_login<(%s)'''
    cur.execute(sql_delete, (start_obj,))

def insert(cur, deviceID, id, name, date, last_login):
    sql_insert = '''INSERT INTO public.devices (device_id, id, displayname, registration, last_login)
                    VALUES (%s, %s, %s, %s, %s)'''
    cur.execute(sql_insert, (deviceID, id, name, date, last_login))

def update(cur, deviceID, last_login):
    sql_update = '''update public.devices set last_login=(%s) where device_id=(%s)'''
    cur.execute(sql_update, (last_login, deviceID))

def insert_devices(conn, devices, file_schema, active_period):
    validate_all(devices, file_schema)
    active_devices = list_active_devices(devices, active_period)
    cur = conn.cursor()
    for device in devices:
        id = device['id']
        deviceID = device['deviceId']
        name = device['displayName']
        date = create_date_obj(device['registrationDateTime'])
        last_login = create_date_obj(device['approximateLastSignInDateTime'])
        sql_check = '''select exists(select device_id from public.devices where device_id=(%s))'''
        cur.execute(sql_check, (deviceID,))
        if cur.fetchone()[0] is False:
            insert(cur, deviceID, id, name, date, last_login)
        else:
            update(cur, deviceID, last_login)
    delete_devices(cur, active_period)
    conn.commit()
    cur.close()
    print("The device list has been updated")

    