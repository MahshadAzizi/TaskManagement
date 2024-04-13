from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.models import User
from rest_framework import status


class TestUser(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_user(username, password, phone_number):
        user = User.objects.create_user(
            username=username, password=password, phone_number=phone_number
        )
        context = {
            'user': user,
            'username': user.username,
            'password': password,
            'phone_number': phone_number
        }
        return context

    @staticmethod
    def create_super_user(username, password, phone_number):
        user = User.objects.create_superuser(
            username=username, password=password, phone_number=phone_number
        )
        context = {
            'user': user,
            'username': user.username,
            'password': password,
            'phone_number': phone_number
        }
        return context

    def get_token_ok(self, phone_number, password):
        url = reverse('login')
        resp = self.client.post(
            url,
            {"phone_number": phone_number, "password": password}, HHTP_REMOTE_ADDR='127.0.0.1', format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data['results'])
        self.assertTrue("refresh" in resp.data['results'])
        self.access = resp.data['results']["access"]
        self.refresh = resp.data['results']["refresh"]
        tokens = {'access': self.access, 'refresh': self.refresh}
        return tokens

    def test_login(self):
        user = self.create_user(username='admin3', password='1234', phone_number='09121231231')
        url = reverse('login')
        tokens = self.get_token_ok(user['phone_number'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, data={'phone_number': user['phone_number'], "password": user['password']},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token_not_exist(self):
        url = reverse('login')
        phone_number = '09121231231'
        password = "123"
        resp = self.client.post(
            url,
            {"phone_number": phone_number, "password": password}, HHTP_REMOTE_ADDR='127.0.0.1',
            format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        user = self.create_user('admin3', '1234', '09121231231')
        tokens = self.get_token_ok(user['phone_number'], user['password'])
        url = reverse('logout')
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, {'refresh_token': tokens["refresh"]}, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
