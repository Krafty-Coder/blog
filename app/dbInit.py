import os

import psycopg2
from passlib.hash import sha256_crypt

dbname = os.environ.get('DBASE_NAME')
dbuser = os.environ.get('DBASE_USER')
dbpass = os.environ.get('DBASE_PASS')
dbhost = os.environ.get('DBASE_HOST')
dbport = os.environ.get('DBASE_PORT')

queries = [
    '''
    CREATE TABLE IF NOT EXISTS articles(
    id serial PRIMARY KEY,
    title varchar (100) NOT NULL,
    author varchar (100) NOT NULL,
    body text NOT NULL,
    create_date timestamp default current_timestamp)
    ''',
    '''
    CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    name varchar (50) NOT NULL,
    email varchar (100) NOT NULL,
    username varchar (50) NOT NULL,
    password varchar (100) NOT NULL,
    join_date timestamp default current_timestamp)
    '''
    ]

class Database():
    def __init__(self, db_url):
        self.dburl = db_url
        self.conn = psycopg2.connect(db_url)  # Connecting to the database

    def create_connection(self):
        self.conn = psycopg2.connect(self.dburl)  # Connecting to the database
        self.conn.autocommit = True
        return self.conn

    def close_connection(self):
        return self.conn.close()

    def create_tables(self):
        cur = self.create_connection().cursor()
        for query in queries:
            cur.execute(query)
            self.conn.commit()
        passkey = os.environ.get('ADMIN_PASS')
        password = str(sha256_crypt.hash(str(passkey)))
        # cur.execute(
        #             """INSERT INTO users (name, email, username, password)
        #             VALUES('krafty coder' ,'kraftycoder@gmail.com' ,'krafty-coder' ,%s);""",
        #             (password,))
        # self.conn.commit()
        self.conn.close()
        return "Tables created successfully"

    def destroy_tables(self):
        cursor = self.create_connection().cursor()
        cursor.execute(
            "SELECT table_schema,table_name FROM information_schema.tables "
            " WHERE table_schema = 'public' ORDER BY table_schema,table_name"
        )
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("drop table "+row[1] + " cascade")
        self.conn.commit()
        self.conn.close()


db_url = "dbname={} user={} password={} host={} port={}".format(dbname, dbuser, dbpass, dbhost, dbport)
db = Database(db_url)
db.close_connection()
db.create_tables()

