from configparser import ConfigParser

def get_distance():
    parser = ConfigParser()
    parser.read("config.ini")
    distance =  parser.get('stats', 'distance')
    return int(distance)

def get_delta_time():
    parser = ConfigParser()
    parser.read('config.ini')
    delta_time = parser.get('stats', 'delta_time')
    return int(delta_time)

def get_unlogged_file():
    parser = ConfigParser()
    parser.read("config.ini")
    file = parser.get('stats', 'unlogged_file')
    return file

def get_unused_file():
    parser = ConfigParser()
    parser.read("config.ini")
    file = parser.get('stats', 'unused_file')
    return file

def get_multilogs_file():
    parser = ConfigParser()
    parser.read("config.ini")
    file = parser.get('stats', 'multilogs_file')
    return file

def get_user_unregdev_file():
    parser = ConfigParser()
    parser.read("config.ini")
    file = parser.get('stats', 'user_unregdev_file')
    return file