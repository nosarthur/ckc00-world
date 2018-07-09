from django.test import TestCase

from api.models import MyUser


class MyUserModelTest(TestCase):

    def test_save_user(self):
        u = MyUser(gender='M', email='a@b.com', password='abc',
                   first_name='John', last_name='Doe')
        u.save()
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(u.get_full_name(), 'John Doe')
        self.assertEqual(u.get_short_name(), 'John')

    def test_create_user(self):
        # normal usage
        u = MyUser.objects.create_user(email='a@b.com', password='aaa', gender='F', first_name='Jane', last_name='Doe')
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(u.is_admin, False)
        self.assertEqual(u.is_active, True)

        # cannot create super user, even if requested
        u = MyUser.objects.create_user(email='a2@b.com', password='aaa',
            gender='F', first_name='Jane', last_name='Doe', is_admin=True)
        self.assertEqual(u.is_admin, False)
        self.assertEqual(u.is_active, True)
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 2)


