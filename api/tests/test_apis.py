from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from cities_light.models import City, Region, Country

from api.models import MyUser, Division, Tag


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
            {'email': '2@b.com', 'password': '2'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.token2 = resp.data['token']

        resp = self.client.post(reverse('get-jwt'),
            {'email': 'admin@b.com', 'password': 'admin'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.admin_token = resp.data['token']

    # FIXME: add more permission tests

    def test_unauthorized_list(self):
        resp = self.client.get(reverse('myuser-list'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_authorized_list(self):
        # regular user
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.get(reverse('myuser-list'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertContains(resp, '1@b.com')
        self.assertContains(resp, '2@b.com')
        self.assertContains(resp, 'admin@b.com')
        self.assertEqual(MyUser.objects.count(), 3)
        # admin
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.get(reverse('myuser-list'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertContains(resp, '1@b.com')
        self.assertContains(resp, '2@b.com')
        self.assertContains(resp, 'admin@b.com')

    def test_unauthorized_CRUD(self):
        resp = self.client.post(reverse('myuser-list'),
            data=self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)
        resp = self.client.get(reverse('myuser-detail', args=['1']), format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)
        resp = self.client.patch(reverse('myuser-detail', args=['1']),
            {'first_name': 'new'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MyUser.objects.count(), 3)
        resp = self.client.delete(reverse('myuser-detail', args=['1']),
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_regular_user_read(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.get(reverse('myuser-detail', args=['1']), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertContains(resp, '1@b.com')
        self.assertNotContains(resp, '2@b.com')

    def test_admin_read(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.get(reverse('myuser-detail', args=['2']), format='json')
        # print(reverse('myuser-detail', args=['2']))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertContains(resp, '2@b.com')

    def test_regular_user_cannot_update_his_admin_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        self.client.patch(reverse('myuser-detail', args=['1']),
            {'is_staff': True, 'is_superuser': True}, format='json')
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertFalse(u1.is_staff)
        self.assertFalse(u1.is_superuser)

    def test_admin_user_cannot_update_other_admin_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        self.client.patch(reverse('myuser-detail', args=['1']),
            {'is_staff': True, 'is_superuser': True}, format='json')
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertFalse(u1.is_staff)
        self.assertFalse(u1.is_superuser)

    def test_regular_user_update(self):
        # owner
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.patch(reverse('myuser-detail', args=['1']),
            {'first_name': 'supernerdy'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 3)
        self.assertContains(resp, 'supernerdy')
        self.assertNotContains(resp, 'A1')
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertEqual(u1.first_name, 'supernerdy')

        # not owner should fail
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        resp = self.client.patch(reverse('myuser-detail', args=['1']),
            {'first_name': 'new'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MyUser.objects.count(), 3)

    def test_admin_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.patch(reverse('myuser-detail', args=['1']),
            {'first_name': 'supernerdy'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 3)
        self.assertContains(resp, 'supernerdy')
        self.assertNotContains(resp, 'A1')

    def test_regular_user_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        resp = self.client.delete(reverse('myuser-detail', args=['1']),
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.delete(reverse('myuser-detail', args=['1']),
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MyUser.objects.count(), 2)

    def test_other_regular_user_cannot_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        resp = self.client.put(reverse('myuser-set-password', args=['1']),
            {'old_password': '1',
             'new_password': 'newnew'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertTrue(u1.check_password('1'))

    def test_self_cannot_change_password_without_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.put(reverse('myuser-set-password', args=['1']),
            {'old_password': 'wrong password',
             'new_password': 'newnew'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertTrue(u1.check_password('1'))
        resp = self.client.put(reverse('myuser-set-password', args=['1']),
            { 'new_password': 'newnew'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_self_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.put(reverse('myuser-set-password', args=['1']),
            {'old_password': '1',
             'new_password': 'newnew'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        u1 = MyUser.objects.get(email='1@b.com')
        self.assertTrue(u1.check_password('newnew'))


class CityTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        MyUser.objects.create_superuser(email='admin@b.com', gender='F',
            first_name='Ace', last_name='Boss', password='admin')
        self.u1 = MyUser.objects.create_user(email='1@b.com', gender='M', first_name='A1',
            last_name='B1', password='pp')
        # get token
        resp = self.client.post(reverse('get-jwt'),
            {'email': '1@b.com', 'password': 'pp'},
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

        # create city
        country = Country.objects.create(name='utopia')
        region = Region.objects.create(name='a Region', country=country)
        City.objects.create(name='a City', region=region, country=country)
        City.objects.create(name='City2', region=region, country=country)

    def test_update_city_self(self):
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.city, None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        resp = self.client.patch(reverse('myuser-detail', args=['2']),
            {'city': {'pk': 1}}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.city.name, 'a City')
        self.assertEqual(self.u1.country.name, 'utopia')

    def test_update_city_admin(self):
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.city, None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.admin_token)
        resp = self.client.patch(reverse('myuser-detail', args=['2']),
            {'city': {'pk': 2}}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.city.name, 'City2')
        self.assertEqual(self.u1.country.name, 'utopia')


class GenderAndDivisionTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        country1 = Country.objects.create(name='utopia')
        region1 = Region.objects.create(name='a Region', country=country1)
        city1 = City.objects.create(name='a City', region=region1, country=country1)
        country2 = Country.objects.create(name='utopia2')
        region2 = Region.objects.create(name='Region2', country=country2)
        city2 = City.objects.create(name='City2', region=region2, country=country2)
        self.d1 = Division.objects.create(name='lit&art', number='2')
        self.d2 = Division.objects.create(name='mixed', number='1')

        self.u1 = MyUser.objects.create_user(email='1@b.com', gender='M',
            first_name='A1', last_name='B1', division=self.d1, password='111',
            city=city1, country=country1)
        u2 = MyUser.objects.create_user(email='2@b.com', gender='M',
            first_name='A2', city=city1, country=country1,
            last_name='B2', division=self.d2)
        u3 = MyUser.objects.create_user(email='3@b.com', gender='M',
            first_name='A3', city=city2, country=country2,
            last_name='B3', division=self.d1)
        u0 = MyUser.objects.create_superuser(email='admin@b.com', gender='F',
            city=city1, country=country1,first_name='Ace', last_name='Boss',
            password='admin', division=self.d1)
        t1 = Tag.objects.create(name='dog')
        t2 = Tag.objects.create(name='pig')
        u0.tags.add(t1)
        self.u1.tags.add(t2)
        u2.tags.add(t1)
        u3.tags.add(t1)

    def test_country_get_all(self):
        resp = self.client.get(
            reverse('gender-country'),
            format='json')
        self.assertEqual(resp.json()['country'],
            [{'utopia': [1, 2]}, {'utopia2': [0, 1]}])

    def test_country_query_division(self):
        resp = self.client.get(
            reverse('gender-country'),
            {'name':'lit&art', 'number': '2'},
            format='json')
        self.assertEqual(resp.json()['country'],
            [{'utopia': [1, 1]}, {'utopia2': [0, 1]}])

    def test_tag_get_all(self):
        resp = self.client.get(
            reverse('gender-tag'),
            format='json')
        self.assertEqual(resp.json()['tag'],
            [{'dog': [1, 2]}, {'pig': [0, 1]}])

    def test_tag_query_division(self):
        resp = self.client.get(
            reverse('gender-tag'),
            {'name':'lit&art', 'number': '2'},
            format='json')
        self.assertEqual(resp.json()['tag'],
            [{'dog': [1, 1]}, {'pig': [0, 1]}])

    def test_update_division(self):
        resp = self.client.post(reverse('get-jwt'),
            {'email': '1@b.com', 'password': '111'},
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        self.token1 = resp.data['token']

        self.u1.refresh_from_db()
        self.assertEqual(self.u1.division, self.d1)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        self.client.patch(reverse('myuser-detail', args=['1']),
            {
                'first_name': 'junk',
                'division': {'pk': 2}
            }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.first_name, 'junk')
        self.assertEqual(self.u1.division, self.d2)
        self.assertEqual(Division.objects.count(), 2)
