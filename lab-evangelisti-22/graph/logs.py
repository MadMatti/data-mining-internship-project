import requests
import json
from datetime import datetime, timedelta
import sys
from jsonschema import validate

def list_logs(token, timeframe, conn, file_schema):
    today = datetime.now()
    start_date = (today - timedelta(days=timeframe, hours=today.hour, minutes=today.minute, seconds=today.second)).strftime("%Y-%m-%dT%H:%M:%SZ")
    endpoint = "https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=createdDateTime ge " + start_date
    headers = {'Authorization': 'Bearer ' + token}
    next_link = endpoint
    while next_link is not None:
        print("Retrieving information from Azure...")
        logs = requests.get(next_link, headers=headers).json()
        insert_logs(conn, logs['value'], file_schema)
        if "@odata.nextLink" in logs:
            next_link = logs['@odata.nextLink']
        else:
            next_link = None

def validate_all(response, file_schema):
    print("Validating the API response...")
    logs = response
    with open(file_schema, "r") as f:
        schema = json.load(f)
    for log in logs:
        try:
            validate(log, schema)
        except Exception as err:
            sys.exit("Error: " + str(err))

def create_date_obj(dateString):
    if dateString is None: return None
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    date_obj = datetime.strptime(dateString, date_format)
    return date_obj

def insert(cur, id, date, user_id, user_name, device_id, device_name, city, state, altitude, latitude, longitude):
    sql_insert = '''INSERT INTO public.logs (id, createdatetime, user_id, userdisplayname, device_id, devicedisplayname, city, state, altitude, latitude, longitude)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cur.execute(sql_insert, (id, date, user_id, user_name, device_id, device_name, city, state, altitude, latitude, longitude))

def update(cur, id, city, state, altitude, latitude, longitude):
    sql_update = '''update public.logs 
                    set city=(%s),
                        state=(%s),
                        altitude=(%s),
                        latitude=(%s),
                        longitude=(%s)
                    where id=(%s)'''
    cur.execute(sql_update, (city, state, altitude, latitude, longitude, id))

def refresh_view(cur):
    sql_refresh = '''REFRESH MATERIALIZED VIEW PUBLIC.log_difference'''
    cur.execute(sql_refresh)

def insert_logs(conn, logs, file_schema):
    validate_all(logs, file_schema)
    print("Adding logs to the database")
    cur = conn.cursor()
    for log in logs:
        id = log['id']
        date = create_date_obj(log['createdDateTime'])
        user_name = log['userDisplayName']
        user_id = log['userId']
        device_id = log['deviceDetail']['deviceId']
        device_name = log['deviceDetail']['displayName']
        city = log['location']['city']
        state = log['location']['state']
        altitude = log['location']['geoCoordinates']['altitude']
        latitude = log['location']['geoCoordinates']['latitude']
        longitude = log['location']['geoCoordinates']['longitude']
        if device_id == "": device_id = None
        if device_name == "": device_name = None
        if city == "": city = None
        if state == "": state = None
        sql_check = '''select exists(select id from public.logs where id=(%s))'''
        cur.execute(sql_check, (id,))
        if cur.fetchone()[0] is False:
            insert(cur, id, date, user_id, user_name, device_id, device_name, city, state, altitude, latitude, longitude)
        else:
            update(cur, id, city, state, altitude, latitude, longitude)
    refresh_view(cur)
    conn.commit()
    cur.close()
    print("Logs until " + str(logs[-1]['createdDateTime']) + " have been added to the database\n")
