import conf
import database
import network
import graph
import stats
from colorama import Fore, init
init()
import sys
import json
import pandas
import tabulate

def test_db():
    params = conf.config.config()
    c = database.connect.connect(params)
    if c is not None:
        print("Succesfully connected to the database")
    else:
        print("Error in database connection")

def help():
    print(Fore.YELLOW + "USAGE:" + Fore.RESET)
    print("command [arguments]")
    print(Fore.YELLOW + "COMMANDS:" + Fore.RESET)
    print(Fore.GREEN + '{:<30}'.format('help') + Fore.RESET + '{:<40}'.format('List all available commands'))
    print(Fore.GREEN + '{:<30}'.format('db-test') + Fore.RESET + '{:<40}'.format('Test database connection'))
    print(Fore.GREEN + '{:<30}'.format('db-mig-status') + Fore.RESET + '{:<40}'.format('Print the status of migrations in the file system and in the database'))
    print(Fore.GREEN + '{:<30}'.format('db-mig-execute') + Fore.RESET + '{:<40}'.format('Execute the migrations'))
    print(Fore.GREEN + '{:<30}'.format('ping') + Fore.RESET + '{:<40}'.format('Ping a fixed API and check the correctness of the parameter pong if passed'))
    print(Fore.GREEN + '{:<30}'.format('graph-devices') + Fore.RESET + '{:<40}'.format('Retrive the devices from Graph API, validate and insert them in the db'))
    print(Fore.GREEN + '{:<30}'.format('graph-users') + Fore.RESET + '{:<40}'.format('Retrive the users from Graph API, validate and insert them in the db'))
    print(Fore.GREEN + '{:<30}'.format('graph-logs') + Fore.RESET + '{:<40}'.format('Retrive the logs from Graph API, validate and insert them in the db'))
    print(Fore.GREEN + '{:<30}'.format('stats-unlogged-users') + Fore.RESET + '{:<40}'.format('List the users who have never done a log in a registered device'))
    print(Fore.GREEN + '{:<30}'.format('stats-unused-devices') + Fore.RESET + '{:<40}'.format('List the devices that have never received a log in a specified timeframe'))
    print(Fore.GREEN + '{:<30}'.format('stats-shared-devices') + Fore.RESET + '{:<40}'.format('List the logs done from different users on the devices used from more than one user'))
    print(Fore.GREEN + '{:<30}'.format('stats-users-unregdev') + Fore.RESET + '{:<40}'.format('List the users who have done logs only on unregistered devices'))
    print(Fore.GREEN + '{:<30}'.format('stats-far-logs') + Fore.RESET + '{:<40}'.format('List the logs done in far places in a short time interval'))

def mig_status():
    conn = database.connect.connect(conf.config.config())
    print(Fore.GREEN)
    print("Migrations ready to be executed: ")
    print(database.migrations.list_ready(conf.config.get_rel_path(), conn))
    print(Fore.RED)
    print("Migrations available only in the file system: ")
    print(database.migrations.list_fs_only(conf.config.get_rel_path(), conn))
    print("Migrations available only in the database: ")
    print(database.migrations.list_db_only(conf.config.get_rel_path(), conn))
    print(Fore.RESET)
    if database.migrations.list_fs_only(conf.config.get_rel_path(), conn) or \
       database.migrations.list_db_only(conf.config.get_rel_path(), conn):
        exit(1)
    conn.close()

def mig_execute():
    conn = database.connect.connect(conf.config.config())
    database.migrations.check_create(conn)
    database.migrations.check_insert(conn, conf.config.get_rel_path())
    conn.close()

def ping():
    network.ping.get_only(conf.config.get_url(), conf.config.get_schema())

def ping_check(pong):
    network.ping.get_check(conf.config.get_url(), conf.config.get_schema(), pong)

def graph_users():
    conn = database.connect.connect(conf.config.config())
    graph.users.insert_users(conn, graph.users.list_users(graph.connect.connect(graph.config.get_authority(), graph.config.get_client_id(), 
                             graph.config.get_scope(), graph.config.get_secret())), graph.config.get_users_schema())
    conn.close()

def graph_devices():
    conn = database.connect.connect(conf.config.config())
    graph.devices.insert_devices(conn, graph.devices.list_devices(graph.connect.connect(graph.config.get_authority(), graph.config.get_client_id(), 
                                 graph.config.get_scope(), graph.config.get_secret())), graph.config.get_devices_schema(), graph.config.get_devices_period())
    conn.close()

def graph_logs():
    conn = database.connect.connect(conf.config.config())
    graph.logs.list_logs(graph.connect.connect(graph.config.get_authority(), graph.config.get_client_id(), 
                        graph.config.get_scope(), graph.config.get_secret()), graph.config.get_timeframe(), 
                        conn, graph.config.get_logs_schema())
    conn.close()

def stats_far_logs(period=90):
    conn = database.connect.connect(conf.config.config())
    data = stats.execute_stats.far_logs(conn, stats.config.get_distance(), stats.config.get_delta_time(), period)
    df = pandas.DataFrame(data=data)
    cols = ["id", "user_id", "user_name", "curr_time", "prec_time", "time_diff", "curr_lat", "prec_lat", "curr_long", "prec_long", "dist_diff"]
    print(tabulate.tabulate(df, headers=cols, tablefmt='psql', showindex=False))    
    conn.close()

def stats_unlogged_users(period=90):
    conn = database.connect.connect(conf.config.config())
    data = stats.execute_stats.unlogged_user(conn, period)
    df = pandas.DataFrame(data=data)
    cols = ["user_id", "givenname"]
    print(tabulate.tabulate(df, headers=cols, tablefmt='psql', showindex=False))
    conn.close()

def stats_unused_devices(period=90):
    conn = database.connect.connect(conf.config.config())
    data = stats.execute_stats.unused_devices(conn, period)
    df = pandas.DataFrame(data=data)
    cols = ["device_id", "displayname"]
    print(tabulate.tabulate(df, headers=cols, tablefmt='psql', showindex=False))
    conn.close()

def stats_shared_devices(period=90):
    conn = database.connect.connect(conf.config.config())
    data = stats.execute_stats.multilogs_devices(conn, period)
    df = pandas.DataFrame(data=data)
    cols = ["device_id", "deviceDisplayname", "user_id", "userDisplayname"]
    print(tabulate.tabulate(df, headers=cols, tablefmt='psql', showindex=False))
    conn.close()

def stats_users_unreg_devices(period=90):
    conn = database.connect.connect(conf.config.config())
    data = stats.execute_stats.user_ureg_devices(conn, period)
    df = pandas.DataFrame(data=data)
    cols = ["user_id", "userDisplayname"]
    print(tabulate.tabulate(df, headers=cols, tablefmt='psql', showindex=False))
    conn.close()




if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        #help menu
        help()
    elif len(sys.argv) == 2:
        choice = sys.argv[1]
        if choice == "help":
            help()
        elif choice == "db-test":
            test_db()
        elif choice == "db-mig-status":
            mig_status()
        elif choice == "db-mig-execute":
            mig_execute()
        elif choice == "ping":
            ping()
        elif choice == "graph-users":
            graph_users()
        elif choice == "graph-devices":
            graph_devices()
        elif choice == "graph-logs":
            graph_logs()
        elif choice == "stats-far-logs":
            stats_far_logs()
        elif choice == "stats-unlogged-users":
            stats_unlogged_users()
        elif choice == "stats-unused-devices":
            stats_unused_devices()
        elif choice == "stats-shared-devices":
            stats_shared_devices()
        elif choice == "stats-users-unregdev":
            stats_users_unreg_devices()
        else:
            print("Command " + choice + " not found")
            print("Try the " + Fore.GREEN + "help" + Fore.RESET + " for information about the available commands")
            sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1] == "ping":
        ping_check(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "stats-far-logs":
        stats_far_logs(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "stats-unlogged-users":
        stats_unlogged_users(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "stats-unused-devices":
        stats_unused_devices(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "stats-shared-devices":
        stats_shared_devices(int(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "stats-users-unregdev":
        stats_users_unreg_devices(int(sys.argv[2]))
    else:
        exit("Wrong number of parameter " + str(len(sys.argv)))