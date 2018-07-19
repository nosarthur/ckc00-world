from rest_framework import serializers
from cities_light.models import City

from api.models import MyUser, Division, Tag


class DivisionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Division
        fields = ('url', 'name', 'number',)

    def validate(self, data):
        try:
            name = data['name']
            number = data['number']
        except KeyError:
            raise serializers.ValidationError(f'Division name and number are missing.')
        try:
            d = Division.objects.get(name=name, number=number)
        except Division.DoesNotExist:
            raise serializers.ValidationError(f'Division {name} {number} does not exist.')
        return d


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):
    # FIXME: the write operation is probably broken
    region = serializers.CharField(source='region.name')
    country = serializers.CharField(source='country.name')

    class Meta:
        model = City
        fields = ('name', 'region', 'country')

    def validate(self, data):
        try:
            city_name = data['name']
            region_name = data['region']['name']
            country_name = data['country']['name']
        except KeyError:
            raise serializers.ValidationError(f'City name, region name, and country name are missing.')
        try:
            city = City.objects.get(
                    name=city_name,
                    region__name=region_name,
                    country__name=country_name)
        except City.DoesNotExist:
            raise serializers.ValidationError(f'City {city_name} {region_name} {country_name} does not exist.')
        return city


class UserSerializer(serializers.HyperlinkedModelSerializer):
    division = DivisionSerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    city = CitySerializer(required=False)

    class Meta:
        model = MyUser
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'employer', 'homepage',
                  'division', 'tags', 'city')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.homepage = validated_data.get('homepage', instance.homepage)
        instance.employer = validated_data.get('employer', instance.employer)
        d = validated_data.get('division', None)
        if d:
            instance.division = d
        city = validated_data.get('city', None)
        if city:
            instance.city = city

        instance.save()
        return instance
        

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
