from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse

from api.models import MyUser


class UserTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        MyUser.objects.create_user(email='1@b.com', gender='M', first_name='A1',
            last_name='B1', password='1')
        MyUser.objects.create_user(email='2@b.com', gender='M', first_name='A2',
            last_name='B2', password='2')
        MyUser.objects.create_superuser(email='admin@b.com', gender='F',
            first_name='Ace', last_name='Boss', password='admin')
        self.data = {'email': 'a@b.com', 'password': 'aaa', 'gender': 'M',
                     'first_name': 'John', 'last_name': 'Doe', }

    # FIXME: add more permission tests

    def test_unauthorized_list(self):
        response = self.client.get(reverse('myuser-list'),
                                   format='json')
        self.assertEqual(MyUser.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, '1@b.com')
        self.assertContains(response, '2@b.com')
        self.assertNotContains(response, 'admin@b.com')

    def test_unauthorized_create(self):
        response = self.client.post(reverse('myuser-list'),
            kwargs=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)


class AuthTest(TestCase):
    def test_(self):
        pass


class TokenTest(TestCase):
    pass
