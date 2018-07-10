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
        # get tokens
        resp = self.client.post(reverse('get-jwt'),
            {'email': '1@b.com', 'password': '1'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.token1 = resp.data['token']

        resp = self.client.post(reverse('get-jwt'),
            {'email': 'admin@b.com', 'password': 'admin'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.admin_token = resp.data['token']

    # FIXME: add more permission tests

    def test_unauthorized_list(self):
        resp = self.client.get(reverse('myuser-list'),
                                   format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_authorized_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.get(reverse('myuser-list'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertContains(resp, '1@b.com')
        self.assertContains(resp, '2@b.com')
        self.assertContains(resp, 'admin@b.com')
        self.assertEqual(MyUser.objects.count(), 3)

    def test_unauthorized_create(self):
        resp = self.client.post(reverse('myuser-list'),
            data=self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_unauthorized_read(self):
        pass

    def test_unauthorized_update(self):
        pass

    def test_unauthorized_delete(self):
        pass

    def test_regular_user_create_new_user_with_jwt_should_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.post(reverse('myuser-list'),
                                data=self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_admin_user_create_new_user_with_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.post(reverse('myuser-list'),
                                data=self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 4)

    def test_create_with_invalid_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + 'junk token')
        resp = self.client.post(reverse('myuser-list'),
                                data=self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_regular_user_get_jwt(self):
        pass


class TokenTest(TestCase):
    pass
