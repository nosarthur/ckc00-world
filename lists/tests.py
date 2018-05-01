from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.

class HomepageTest(TestCase):
    def test_root_url_resolve(self):
        found = resolve('/')
        assert found.func == home_page
