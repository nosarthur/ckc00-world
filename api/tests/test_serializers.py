from django.test import TestCase

from api.serializers import DivisionSerializer


class DivisionSerializerTest(TestCase):
    s = DivisionSerializer(data={'name': 'mixed', 'number': '5'})
    assert s.is_valid()


