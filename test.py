# Test file
import unittest
from passlib.hash import sha256_crypt
import os

import psycopg2
import app
from app.models.users import User_Model
from app import create_app
from flask import Flask
from app.dbInit import Database


dbname = os.environ.get('DB_NAME')
dbuser = os.environ.get('DB_USER')
dbpass = os.environ.get('DB_PASS')
dbhost = os.environ.get('DB_HOST')

db_url = "dbname={} user={} password={} host={} port=5432".format(dbname, dbuser, dbpass, dbhost)
app = Flask(__name__)


class FlaskTestAppCases(unittest.TestCase):

    def setUp(self):
        self.db = Database("test_db")
        self.conn = db.create_connection()
        self.db.create_tables()
        self.cur = conn.cursor()
        self.app = create_app(config_name="testing")
        self.tester = self.app.test_client()
        self.user = User_Model()
        password = str(sha256_crypt.encrypt(str("adminpass")))
        self.user.post('admin','admin@gmail.com','admin',password)
        self.user.save()

        # Commit to DB
        self.conn.commit()
        # Close Connection
        self.conn.close()

    def tearDown(self):
        return self.db.destroy_tables()

    #Ensure that Flask was set up correctly
    def test_index(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    # Test for login working correctly with the right credentials
    def test_correct_login(self):
        response = self.tester.post(
            '/login',
            data=dict(username="admin", password="adminpass"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in', response.data)

    # Test for login working correctly with the wrong credentials
    def test_incorrect_login(self):
        password = str(sha256_crypt.hash(str("wrongagain")))
        response = self.tester.post(
            '/login',
            data=dict(username="wrong", password="adminpass"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found', response.data)


    # Test for logout working perfectly
    def test_correct_logout(self):
        self.tester.post(
            '/login',
            data=dict(username="admin", password="adminpass"),
            follow_redirects=True
        )
        response = self.tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You have successfully logged out', response.data)


    def test_dashboard_requires_login(self):
        self.tester.post('/dashboard', follow_redirects=True)
        response = self.tester.get('/login', follow_redirects=True)
        self.assertTrue(b'Password or username incorrect, Invalid login', response.data)

    # Show articles on the main page
    def test_articles_display_on_dashboard(self):
        response = self.tester.post(
            '/login',
            data=dict(username="admin", password="adminpass"),
            follow_redirects=True
        )
        self.assertIn(b'Welcome admin', response.data)


if __name__ == '__main__':
    unittest.main()

