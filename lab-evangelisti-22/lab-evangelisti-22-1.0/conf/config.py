from configparser import ConfigParser

def config(filename="config.ini", section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_url():
    parser = ConfigParser()
    parser.read("config.ini")
    url = parser.get('ping', 'url')
    return url

def get_schema():
    parser = ConfigParser()
    parser.read("config.ini")
    fname = parser.get('ping', 'schema')
    return fname

def get_rel_path():
    parser = ConfigParser()
    parser.read("config.ini")
    rel_path = parser.get('migrations', 'rel_path')
    return rel_path