import os

import psycopg2

dbname = os.environ.get('DB_NAME')
dbuser = os.environ.get('DB_USER')
dbpass = os.environ.get('DB_PASS')
dbhost = os.environ.get('DB_HOST')
def conn():
    return psycopg2.connect("dbname={} user={} password={} host={} port=5432".format(dbname, dbuser, dbpass, dbhost))  # Connecting to the database

def cur():
    return conn().cursor()  # Activate connection using the cursor


cur().execute('''CREATE TABLE IF NOT EXISTS articles(
    id serial PRIMARY KEY,
    title varchar (50) NOT NULL,
    author varchar (100) NOT NULL,
    body text NOT NULL,
    create_date timestamp default current_timestamp
) ''')
conn().commit()


cur().execute('''CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    name varchar (50) NOT NULL,
    email varchar (100) NOT NULL,
    username varchar (50) NOT NULL,
    password varchar (100) NOT NULL,
    join_date timestamp default current_timestamp
) ''')
conn().commit()

