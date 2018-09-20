import psycopg2

conn = psycopg2.connect("dbname=d49pt4ur37g33c user=oqrnhavmylzeql password=290ca06f7d3667c7ebeb2d89f1ed502ce9db4ff7d91d2fd4269e92f7052a2283 host=ec2-54-225-241-25.compute-1.amazonaws.com port=5432")  # Connecting to the database
cur = conn.cursor()  # Activate connection using the cursor

try:
    cur.execute('''CREATE TABLE IF NOT EXISTS articles(
        id serial PRIMARY KEY,
        title varchar (50) NOT NULL,
        author varchar (100) NOT NULL,
        body text NOT NULL,
        create_date timestamp default current_timestamp
    ) ''')
    conn.commit()
except:
    print('Table already exists')

try:
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id serial PRIMARY KEY,
        name varchar (50) NOT NULL,
        email varchar (100) NOT NULL,
        username varchar (50) NOT NULL,
        password varchar (100) NOT NULL,
        join_date timestamp default current_timestamp
    ) ''')
    conn.commit()
except:
    print('Table already exists')

