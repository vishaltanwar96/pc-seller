import random
import string
from unittest import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DJValidationError

from users.serializers import UserSerializer

User = get_user_model()


class PasswordValidationTests(TestCase):

    def test_strong_password(self):

        self.assertEqual(validate_password('VeryStrongPassword@%19*@9'), None)

    def test_unqualified_password(self):

        with self.assertRaises(DJValidationError):
            validate_password('abc')


class UserRegistrationAPITests(APITestCase):

    def setUp(self):
        self.url = reverse('user-registration')

    def test_create_user(self):

        response = self.client.post(
            self.url,
            {
                'email': 'vishal.tanwar@somedomain.com',
                'first_name': 'Vishal',
                'last_name': 'Tanwar',
                'password': 'SomeUser@123',
                'confirm_password': 'SomeUser@123'
            }
        )
        user = User.objects.get()
        self.assertEqual(response.data, UserSerializer(instance=user).data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_bad_email(self):

        response = self.client.post(
            self.url,
            {
                'email': 'vishal.tanwar',
                'first_name': 'Vishal',
                'last_name': 'Tanwar',
                'password': 'SomeUser@123',
                'confirm_password': 'SomeUser@123'
            }
        )
        self.assertEqual(response.data, {"email": ["Enter a valid email address."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_fname_lname_validation(self):

        random_chars = ''.join(random.choices(string.ascii_lowercase+string.ascii_uppercase, k=51))
        response = self.client.post(
            self.url,
            {
                'email': 'vishal.tanwar@somedomain.com',
                'first_name': random_chars,
                'last_name': random_chars,
                'password': 'SomeUser@123',
                'confirm_password': 'SomeUser@123'
            }
        )
        self.assertEqual(
            response.data,
            {
                "first_name": ["Ensure this field has no more than 50 characters."],
                "last_name": ["Ensure this field has no more than 50 characters."]
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_equals_confirm_password(self):

        response = self.client.post(
            self.url,
            {
                'email': 'vishal.tanwar@somedomain.com',
                'first_name': 'Vishal',
                'last_name': 'Tanwar',
                'password': 'SomeUser@123',
                'confirm_password': 'SomeUser@12'
            }
        )
        self.assertEqual(response.data, {"confirm_password": ["Password must match confirm password"]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITests(APITestCase):

    def setUp(self):

        self.url = reverse('login')

    def test_login_with_admin_user(self):

        password = 'SuperSecretPassword@123'
        email = 'vishal.tanwar@somedomain.com'
        User.objects.create_superuser(email=email, password=password, first_name='Vishal', last_name='Tanwar')
        response = self.client.post(self.url, {'email': email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_non_admin_user(self):

        password = 'SuperSecretPassword@123'
        email = 'vishal.tanwar@somedomain.com'
        User.objects.create_user(email=email, password=password, first_name='Vishal', last_name='Tanwar')
        response = self.client.post(self.url, {'email': email, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_nonexistent_user(self):

        response = self.client.post(self.url, {'email': 'user@somedomain.com', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"non_field_errors": ["Unable to log in with provided credentials."]})
