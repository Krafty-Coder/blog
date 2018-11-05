# Test file
import unittest
import os

import psycopg2
import app
from flaskext.mysql import MySQL


dbhost = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
dbuser = os.environ.get('DB_USER')
dbpass = os.environ.get('DB_PASS')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'adminray'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conn = psycopg2.connect("dbname={} user={} password={} host={} port=5432".format(dbname, dbuser, dbpass, dbhost))  # Connecting to the database
cur = conn.cursor()
mysql = MySQL()
mysql.init_app(app)


class FlaskTestAppCases(unittest.TestCase):
    mysql = MySQL()
    mysql.init_app(app)

    def setUp(self):
        self.cur = mysql.connection.cursor()
        self.cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES('admin',\
            'admin@gmail.com', 'admin', 'adminpass')")

        # Commit to DB
        mysql.connection.commit()

        # Close Connection

    def tearDown(self):
        return self.cur.drop

    #Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    # Test for login working correctly with the right credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="adminpass"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in', response.data)

    # Test for login working correctly with the wrong credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrongagain"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found', response.data)


    # Test for logout working perfectly
    def test_correct_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You have successfully logged out', response.data)


    def test_dashboard_requires_login(self):
        tester = app.test_client(self)
        tester.post('/dashboard', follow_redirects=True)
        response = tester.get('/login', follow_redirects=True)
        self.assertTrue(b'Unauthorised, Please log in to continue to this page', response.data)

    # Show articles on the main page
    def test_articles_display_on_dashboard(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Dashboard Welcome admin', response.data)


if __name__ == '__main__':
    unittest.main()

