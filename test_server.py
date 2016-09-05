import unittest
from server import app
from model import db, connect_to_db
import os

key = os.environ['FLASK_SECRET']

class FlaskTests(unittest.TestCase):
    """Test cases for testing Flask routes."""

    def setUp(self):
        """Set up for every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        """Testing sign in page."""

        self.client = app.test_client()

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Search for a race:', result.data)

        
    def test_not_signed_in(self):
        """ Test homepage for when user is not logged in."""

        self.client = app.test_client()
        result = self.client.get('/')
        self.assertNotIn('Log Out', result.data)


    def test_registration(self):
        """Tests registration page."""

        self.client = app.test_client()
        result = self.client.get('/register')
        self.assertIn('Thanks for your interest!', result.data)


    def test_login_page(self):
        """Tests sign in page."""

        self.client = app.test_client()
        result = self.client.get('/login')
        self.assertIn('User ID:', result.data)


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests taht use the database."""

    def setUp(self):
        """Set up for every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = key

        # Connect to test database.
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data.
        db.create_all()
        example_data()
        

    def tearDown(self):
        """Do at the end of every test."""

        db.session.close()
        db.drop_all()


    # def test_successful_login(self):
    #     """User successfully logged in."""








############################
if __name__ == "__main__": 
    unittest.main()