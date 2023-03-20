from django.contrib.auth.models import User
from .models import House
from rest_framework import status
from rest_framework.test import APITestCase


class HouseListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_houses(self):
        adam = User.objects.get(username='adam')
        House.objects.create(owner=adam, title='a title')
        response = self.client.get('/houses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/houses/', {'title': 'a title'})
        count = House.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_house(self):
        response = self.client.post('/houses/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
