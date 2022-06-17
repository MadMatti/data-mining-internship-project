from configparser import ConfigParser

def get_authority():
    parser = ConfigParser()
    parser.read("config.ini")
    authority = parser.get('graph', 'authority')
    return authority

def get_client_id():
    parser = ConfigParser()
    parser.read("config.ini")
    id = parser.get('graph', 'client_id')
    return id

def get_scope():
    parser = ConfigParser()
    parser.read("config.ini")
    scope = parser.get('graph', 'scope')
    return [scope]

def get_secret():
    parser = ConfigParser()
    parser.read("config.ini")
    secret = parser.get('graph', 'secret')
    return secret

def get_users_schema():
    parser = ConfigParser()
    parser.read("config.ini")
    users_schema = parser.get('graph', 'users_schema')
    return users_schema

def get_devices_schema():
    parser = ConfigParser()
    parser.read("config.ini")
    devices_schema = parser.get('graph', 'devices_schema')
    return devices_schema

def get_devices_period():
    parser = ConfigParser()
    parser.read('config.ini')
    period = parser.get('graph', 'devices_period')
    return int(period)

def get_timeframe():
    parser = ConfigParser()
    parser.read('config.ini')
    timeframe = parser.get('logs', 'timeframe')
    return int(timeframe)

def get_logs_schema():
    parser = ConfigParser()
    parser.read('config.ini')
    logs_schema = parser.get('logs', 'logs_schema')
    return logs_schema
