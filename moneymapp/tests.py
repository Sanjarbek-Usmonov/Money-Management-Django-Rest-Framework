from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class UserOrRegisterTest(APITestCase):
    def test_create_account(self):
        url = reverse('register')
        data = {'username': 'Sanjarbek', 'password': '123'}
        response =  self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('token'), 40)