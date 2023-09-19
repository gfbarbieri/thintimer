# user_auth/tests.py

###############################################################################
# IMPORTS
###############################################################################

# Third-party imports: Django natives.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Third-party imports: Django DRF.
from rest_framework import status
from rest_framework.test import APITestCase

###############################################################################
# DRF API TEST CASES
###############################################################################

"""
Notes on APITestCase from Django REST framework.

`APITestCase` is a class provided by Django REST framework's testing framework
for writing test cases specifically tailored to testing APIs. It's designed to
make it easier to write and execute tests for Django REST framework views and
endpoints.

Here's what `APITestCase` provides:
1. **Test Client**: `APITestCase` includes a test client that can be used to
make HTTP requests to your API endpoints just like a regular Django test client
for web views. This allows you to simulate API requests and responses in your
tests.

2. **Assertion Helpers**: It includes assertion methods like `assertEqual`,
`assertNotEqual`, `assertIsNone`, etc., which can be used to validate the
responses received from API endpoints.

3. **Database Handling**: It sets up and tears down the database state for your
tests, ensuring that each test starts with a clean slate. It provides methods
like `setUp` and `tearDown` for this purpose.

4. **Authentication**: `APITestCase` provides authentication methods, like 
`self.client.login()`, that allow you to simulate user authentication in your
API tests.

5. **Serialization**: It simplifies the process of sending data to your API
endpoints by allowing you to serialize data and send it in the request body.

6. **Response Handling**: You can easily access and validate the response data
and status codes returned by API endpoints.

In the code, `APITestCase` is used as the base class for test
cases to take advantage of these features when testing API-related functionality
in a Django REST framework application. This makes it convenient to write and
run tests for API views and ensures that your tests are properly isolated
and have access to necessary utilities for making API requests and performing
assertions.

"""

# Test class for user login.
class UserLoginTests(APITestCase):
    """
    Test cases for user login functionality.
    """
    def setUp(self):
        # Create a user for testing with a username and password.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Define the URL for the user login endpoint.
        self.url = reverse('user_login')

    def test_valid_login(self):
        """
        Test a valid user login attempt.

        Sends a POST request with valid login data.
        Expects a successful login (HTTP 200 OK) response.
        """
        # Create data for a valid login attempt.
        data = {'username': 'testuser', 'password': 'testpass'}
        # Send a POST request to the login endpoint with the test data.
        response = self.client.post(self.url, data, format='json')
        
        # Check if the response status code is HTTP 200 OK for a successful login.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        """
        Test an invalid user login attempt.

        Sends a POST request with invalid login data (wrong password).
        Expects an unauthorized login (HTTP 401 UNAUTHORIZED) response.
        """
        # Create data for an invalid login attempt (wrong password).
        data = {'username': 'testuser', 'password': 'wrongpass'}
        # Send a POST request to the login endpoint with the test data.
        response = self.client.post(self.url, data, format='json')

        # Check if the response status code is HTTP 401 UNAUTHORIZED for an unsuccessful login.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Test class for user logout.
class UserLogoutTests(APITestCase):
    """
    Test cases for user logout functionality.
    """
    def setUp(self):
        # Create a user for testing with a username and password.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Log in the user for testing purposes.
        self.client.login(username='testuser', password='testpass')
        # Define the URL for the user logout endpoint.
        self.url = reverse('user_logout')

    def test_logout(self):
        """
        Test user logout functionality.

        Sends a POST request to the logout endpoint to log out the user.
        Expects a successful logout (HTTP 200 OK) response.
        """
        # Send a POST request to the logout endpoint to log out the user.
        response = self.client.post(self.url, format='json')

        # Check if the response status code is HTTP 200 OK for a successful logout.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test class for user signup.
class UserSignUpTests(APITestCase):
    """
    Test cases for user signup functionality.
    """
    def setUp(self):
        # Define the URL for the user signup endpoint.
        self.url = reverse('user_signup')

    def test_valid_signup(self):
        """
        Test a valid user signup.

        Sends a POST request with valid signup data.
        Expects a successful signup (HTTP 201 CREATED) response.
        """
        # Create data for a valid signup (email and password provided).
        data = {'email': 'testuser@example.com', 'password': 'testpass'}
        # Send a POST request to the signup endpoint with the test data.
        response = self.client.post(self.url, data, format='json')

        # Check if the response status code is HTTP 201 CREATED for a successful signup.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if a user with the provided email exists in the database.
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_invalid_signup(self):
        """
        Test an invalid user signup.

        Sends a POST request with invalid signup data (empty email).
        Expects a bad request (HTTP 400 BAD REQUEST) response.
        """
        # Create data for an invalid signup (email not provided).
        data = {'email': '', 'password': 'testpass'}
        # Send a POST request to the signup endpoint with the test data.
        response = self.client.post(self.url, data, format='json')

        # Check if the response status code is HTTP 400 BAD REQUEST for an unsuccessful signup.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if no user was created in the database due to the invalid signup.
        self.assertEqual(User.objects.count(), 0)

# Test class for updating username.
class UpdateUsernameTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('update_username')

    def test_valid_username_update(self):
        data = {'new_username': 'newtestuser'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newtestuser')

    def test_invalid_username_update(self):
        data = {'new_username': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Test class for updating email.
class UpdateEmailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('update_email')

    def test_valid_email_update(self):
        data = {'new_email': 'newtestuser@example.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newtestuser@example.com')

    def test_invalid_email_update(self):
        data = {'new_email': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Test class for updating password.
class UpdatePasswordTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('reset_password')

    def test_valid_password_update(self):
        data = {'old_password': 'testpass', 'new_password': 'newtestpass'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_invalid_password_update(self):
        data = {'old_password': 'wrongtestpass', 'new_password': 'newtestpass'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Test class for deleting account.
class DeleteAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('delete_account')

    def test_account_deletion(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
