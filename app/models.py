import os

import psycopg2
from passlib.hash import sha256_crypt

dbname = os.environ.get('DB_NAME')
dbuser = os.environ.get('DB_USER')
dbpass = os.environ.get('DB_PASS')
dbhost = os.environ.get('DB_HOST')

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
    def __init__(self, dburl):
        self.dburl = dburl
        self.conn = None

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
        passkey = os.environ.get('ADMIN_PASS')
        password = str(sha256_crypt.encrypt(passkey))
        cur.execute(
                    """INSERT INTO users (name, email, username, password)
                    VALUES('krafty coder' ,'kraftycoder@gmail.com' ,'krafty-coder' ,%s);""",
                    (password,))
        self.conn.commit()
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


db_url = "dbname={} user={} password={} host={} port=5432".format(dbname, dbuser, dbpass, dbhost)
db = Database(db_url)
db.create_tables()
db.close_connection()

