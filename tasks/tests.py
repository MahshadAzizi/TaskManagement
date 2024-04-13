from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.models import User
from rest_framework import status


class TestTask(APITestCase):
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

    def test_get_all_tasks(self):
        user = self.create_user('admin', '1234', '09121231231')
        url = reverse('tasks')
        tokens = self.get_token_ok(user['phone_number'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_create_task_without_assignee(self):
        assigner = self.create_user('admin', '1234', '09121231231')
        url = reverse('tasks')
        tokens = self.get_token_ok(assigner['phone_number'], assigner['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, data={'title': 'test'},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data, token

    def test_create_task_with_assignee(self):
        assigner = self.create_user('admin', '1234', '09121231231')
        assignee = self.create_user('admin2', '1234', '09121231232')
        url = reverse('tasks')
        tokens = self.get_token_ok(assigner['phone_number'], assigner['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, data={'title': 'test', 'assignee': assignee['username']},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data, assignee['phone_number'], assignee['password']

    def test_update_task_ok(self):
        task, token = self.test_create_task_without_assignee()
        url = reverse('task_detail', kwargs={'pk': task['results']['id']})
        response = self.client.patch(
            url, data={'title': 'test1'},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_delete_task_with_not_permission(self):
        task, phone_number, password = self.test_create_task_with_assignee()
        url = reverse('task_detail', kwargs={'pk': task['results']['id']})
        tokens = self.get_token_ok(phone_number, password)
        token = f'Bearer {tokens["access"]}'
        response = self.client.delete(
            url, data={'title': 'test1'},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        return response.data

    def test_get_task_detail(self):
        task, token = self.test_create_task_without_assignee()
        url = reverse('task_detail', kwargs={'pk': task['results']['id']})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_delete_task(self):
        task, token = self.test_create_task_without_assignee()
        url = reverse('task_detail', kwargs={'pk': task['results']['id']})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data
