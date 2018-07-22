# Test file
from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

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
            data=dict(username="admin", password="admin"),
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

