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
    # FIXME: the write operation is probably broken
    region = serializers.CharField(source='region.name')
    country = serializers.CharField(source='country.name')

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

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.homepage = validated_data.get('homepage', instance.homepage)
        instance.employer = validated_data.get('employer', instance.employer)
        # division
        # city
        city = validated_data.get('city', None)
        if city:
            city_name = city['name']
            region_name = city['region']['name']
            country_name = city['country']['name']

            try:
                instance.city = City.objects.get(
                    name=city_name,
                    region__name=region_name,
                    country__name=country_name)
            except Exception as e:
                raise serializers.ValidationError(f"Cannot find {city_name}, {region_name}, {country_name}: {e}")

        instance.save()
        return instance


class PasswordSerializer:
    pass
