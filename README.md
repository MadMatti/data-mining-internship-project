## Disclaimer
This is the code of the project I developed during my three months internship at Ubroker.

The report of the internship experience can be found on my profile in [this repository](https://github.com/MadMatti/internship-report) 

# lab-evangelisti-2022

Data mining internship project developed in Python. 

The aim of the project is to retrieve data about employee, company devices and logs from Micorosft Graph API. These data are then processed and manipulated thourh the use of SQL and PowerBi. 

## Modules

This project is composed by several modules:

- console.py
### Package conf
- config.py
### Package database
- connect.py
- migration.py
### Package network
- ping.py
### Package graph
- config.py
- connect.py
- devices.py
- logs.py 
- users.py
### Package stats
- config.py
- execute_stats.py

## console.py

This is the main script, it executes the command which as to be passed as a parameter to the script.

## 1) conf
## config.py

This module is used to interact with the `config.ini` file and retrieve information from it.  
- The `config()` function allows to retrive information aboud the database connection
- The `get_url()` function allows to retrive the url of the API
- The `get_schema()` function allows to get the name of the json file containing the json schema used in the validation
- The `get_path()` functions allows to retrive the absolute path of the "migrations" folder
- The `get_rel_path()` function allows to get the relative path of a generic file inside the "migrations" folder 

## 2) database
## connect.py

This module opens the database connection, using the psycopg2 Python library

## migrations.py

This module allows to interact with the database:
- The `check_create()` function checks if the table "migrations" is already present, otherwise create it
- The `filter()` function filters the files in the "migrations" folder and return a list of the files with the wanted format
- The `check_insert()` function executes the SQL files present in the "migrations" folder and, if the execution is successful, add a record in the "migration" table
- The functions `list_ready()`, `list_fs_only()` and `list_db_only()`, respectively allow to list the migrations ready to be executed, the ones available only in the file system and those available only in the database 

## 3) network
## ping.py

This module allows to interrogate the access point by means of a GET method.
- The `get_only()` function sends a GET request to the API url and validate the json response
- `get_check()` integrates the previous function adding a parameter to the API url and checking its correspondence in the json response

The validation is carried out using the validate module of the jsonschema library

## 4) graph
## config.py
This module is used to interact with the `config.ini` file and retrieve from it information useful for this package.

## connect.py
This module is built following the [project](https://github.com/Azure-Samples/ms-identity-python-daemon/tree/master/1-Call-MsGraph-WithSecret) and it opens a connection with microsoft graph using the authority, client_id, scope and secret of the application

## devices.py
This module interrogate the Microsoft Graph API and retrive the list of the devices registered from the company.
The list of devices is validated thorugh the function `validate_all()`.  
The function `list_active_devices()` check the last activity of each device and then all the devices active in the defined timeframe are added to the database. At the same time the devices which have became inactive are removed from it.

## logs.py 
This module interrogate the Microsoft Graph API and retrive the list of all the logs done in a number of days defined in the `config.ini` file.  
The list of logs is validated through the function `validate_all()`.  
The logs are then inserted in the database only if they are not already present in it.

## users.py
This module interrogate the Microsoft Graph API and retrive the list of all the users registered by the company.  
The list of users is validated through the function `validate_all()`.  
The users are then inserted in the database only if they are not already present in it.

## 5) stats
## config.py 
This module is used to interact with the `config.ini` file and retrieve from it information useful for this package.

## execute_stats.py
This module execute some statistics on the data stored in the database:
- `far_logs()` function returns the list of the logs done in two far places done in a short time interval. The distance is calculated using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).  
  The distance and the time interval used to find the logs are defined in the `config.ini` file.
- `unlogged_users()` functions returns the list of the users who have not done any log in the defined time period.
- `unused_devices()` function returns the list of the devices which have not received any log in the defined time period.
- `multilogs_devices()` function returns the list of logs, grouped by user, done on devices that are used from more than one different user.
- `user_ureg_devices()` function return the list of users who have never done a log in a registered defice, i.e., the users how have done logs only in personal devices.  

All the reports of this module can be done in a specific number of days that has to be passed as parameter when running the command. If no parameter is passed, the reports are executed with a default time period of 90 days.

# How to run this project
## Step 1: clone or download this repository
From your command line:  
<pre><code>git clone https://github.com/ubrk/lab-evangelisti-22.git</code></pre>
or download and extract the repository .zip file

## Step 2: install the dependencies
From your command line:  
<pre><code>pip install -r requirements.txt</code></pre>

## Step 3: run the project
Run the `console.py` or `console.py help` command to get a list of the available commands
