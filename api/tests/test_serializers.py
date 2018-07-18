from django.test import TestCase

from api.serializers import DivisionSerializer


class DivisionSerializerTest(TestCase):

    def test(self):
        s = DivisionSerializer(data={'name': 'mixed', 'number': '5'})
        assert s.is_valid()

