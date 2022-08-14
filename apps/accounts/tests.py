from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.enums import UserRole


class UserTest(APITestCase):
    def setUp(self) -> None:
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')

    def test_signup(self):
        self.username = "TEST_USERNAME"
        self.password = "JSDHfq8erh3292!"
        data = {"username": self.username, "password": self.password, "role": UserRole.PROJECT_MANAGER}
        response = self.client.post(self.signup_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], self.username)
        self.assertEqual(response.json()['role'], UserRole.PROJECT_MANAGER)

    def test_signup_repetitive_username(self):
        self.test_signup()
        data = {"username": self.username, "password": self.password, "role": UserRole.PROJECT_MANAGER}
        response = self.client.post(self.signup_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(response.json()['username'], ['A user with that username already exists.'])

    def test_signup_weak_password(self):
        username = "TEST_USERNAME"
        password = "1234"
        response = self.client.post(self.signup_url,
                                    data={"username": username, "password": password, "role": UserRole.DEVELOPER})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(response.json()['password'],
                              ['This password is too short. It must contain at least 8 characters.',
                               'This password is too common.', 'This password is entirely numeric.'])

    def test_signup_invalid_username(self):
        username = "u%"
        password = "JSDHfq8erh3292!"
        response = self.client.post(self.signup_url,
                                    data={"username": username, "password": password, "role": UserRole.DEVELOPER})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(response.json()['username'],
                              ['Enter a valid username.'
                               ' This value may contain only letters, numbers, and @/./+/-/_ characters.'])

    def test_login(self):
        self.test_signup()
        response = self.client.post(self.login_url, data={"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.refresh_token = response.json().get('refresh')
        self.assertTrue(self.refresh_token)
        self.assertTrue(response.json().get('access'))

    def test_login_invalid_credentials(self):
        self.test_signup()
        response = self.client.post(self.login_url, data={"username": self.username, "password": "invalid"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'No active account found with the given credentials')

    def test_refresh_token(self):
        self.test_login()
        response = self.client.post(self.refresh_url, data={"refresh": self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get('refresh'))

    def test_refresh_invalid_token(self):
        response = self.client.post(self.refresh_url, data={"refresh": "invalid"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['detail'], 'Token is invalid or expired')
