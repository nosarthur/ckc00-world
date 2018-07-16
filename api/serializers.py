from rest_framework import serializers
from cities_light.models import City

from api.models import MyUser, Division, Tag


class DivisionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Division
        fields = ('url', 'name', 'number',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'region', 'country')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    division = DivisionSerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    city = CitySerializer(required=False)

    class Meta:
        model = MyUser
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'employer', 'homepage',
                  'division', 'tags', 'city')


class PasswordSerializer:
    pass
