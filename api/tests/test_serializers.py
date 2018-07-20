from django.test import TestCase
from cities_light.models import City, Region, Country

from api.serializers import DivisionSerializer, CitySerializer
from api.models import Division


class DivisionSerializerTest(TestCase):

    def test(self):
        s = DivisionSerializer(data={'name': 'mixed', 'number': '5'})
        self.assertFalse(s.is_valid())
        d = Division.objects.create(name='mixed', number='5')
        s = DivisionSerializer(data={'pk': 1})
        # s.is_valid()
        # print(s.errors)
        self.assertTrue(s.is_valid())
        self.assertEqual(d, s.validated_data['pk'])


class CitySerializerTest(TestCase):

    def test(self):
        s = CitySerializer(data={'pk': '1'})
        self.assertFalse(s.is_valid())

        country = Country.objects.create(name='utopia')
        region = Region.objects.create(name='midguard', country=country)
        city = City.objects.create(name='sin city', region=region, country=country)
        s = CitySerializer(data={'pk': 1})
        # s.is_valid()
        # print(s.errors)
        self.assertTrue(s.is_valid())
        self.assertEqual(city, s.validated_data['pk'])

        s = CitySerializer(data={'pk': 2})
        self.assertFalse(s.is_valid())

