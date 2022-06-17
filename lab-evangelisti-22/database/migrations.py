import os
import re
from datetime import datetime
import sys

def check_create(conn):
    cur = conn.cursor()
    sql_create = '''CREATE TABLE IF NOT EXISTS migrations (version text PRIMARY KEY, apply_at timestamptz NOT NULL)'''
    sql_set = '''SET timezone = 'Europe/Rome\''''
    cur.execute(sql_create)
    cur.execute(sql_set)
    cur.close()

def filter (path):
    files = [f for f in os.listdir(path) if re.match('.*(\.sql)$',f)]
    date_format = "%Y%m%d%H%M"
    for f in files:
        try:
            datetime.strptime(f.rsplit('.')[0], date_format)
        except:
            files.remove(f)
    files.sort()
    return files

def check_insert(conn, rel_path):
    migrations = list_ready(rel_path, conn)
    if not migrations: print("There are no migrations ready to be executed")
    cur = conn.cursor()
    sql_check = '''select exists(select version from public.migrations where version=(%s))'''
    for mig in migrations:
        cur.execute(sql_check, (mig,))
        if cur.fetchone()[0] is False:
            sql_last = '''SELECT EXISTS (SELECT 1 FROM public.migrations WHERE version > (%s))'''
            cur.execute(sql_last, (mig,))

            if cur.fetchone()[0] is False:
                fname = rel_path + os.sep + mig + ".sql"
                with open(fname, 'r') as file:
                    try:
                        cur.execute(file.read())
                    except Exception as err:
                        sys.exit("Error: " + str(err))
                sql_insert = '''insert into public.migrations (version, apply_at) values ((%s), current_timestamp)'''
                cur.execute(sql_insert, (mig,))
                conn.commit()
                cur.close()
            else:
                sys.exit("Error: not the most recent migration")
        else:
            sys.exit("Error: migration already exists in the database")

def get_last(conn):
    cur = conn.cursor()
    sql_get_last = '''select max(version) from public.migrations'''
    cur.execute(sql_get_last)
    max = cur.fetchone()[0]
    return max

def list_ready(path, conn):
    mig_fs = []
    for mig in filter(path):
        mig_fs.append(mig.rsplit('.')[0]) 
    last = get_last(conn)
    if last is None:
        return mig_fs
    else:
        mig_ready = [mig for mig in mig_fs if mig > last]
        return mig_ready

def list_fs_only(path, conn):
    mig_fs = []
    for mig in filter(path):
        mig_fs.append(mig.rsplit('.')[0])
    sql_get_mig = '''select version from public.migrations'''
    cur = conn.cursor()
    cur.execute(sql_get_mig)
    mig_db = []
    for mig in cur:
        mig_db.append(mig[0])
    diff_fs_db = []
    if mig_db is None:
        diff_fs_db = mig_fs.copy()
    else:
        diff_fs_db = [mig for mig in mig_fs if mig not in mig_db]
    return diff_fs_db

def list_db_only(path, conn):
    mig_fs = []
    for mig in filter(path):
        mig_fs.append(mig.rsplit('.')[0])
    sql_get_mig = '''select version from public.migrations'''
    cur = conn.cursor()
    cur.execute(sql_get_mig)
    mig_db = []
    for mig in cur:
        mig_db.append(mig[0])
    if mig_db is None:
        diff_db_fs = []
    else:
        diff_db_fs = [mig for mig in mig_db if mig not in mig_fs]
    return diff_db_fs


