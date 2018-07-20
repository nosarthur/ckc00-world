from rest_framework import serializers
from cities_light.models import City

from api.models import MyUser, Division, Tag


class CountrySerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'pk': obj.pk,
            'regions': [{'name': r.name, 'pk': r.pk}
                        for r in obj.region_set.all()]
        }


class RegionSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'pk': obj.pk,
            'cities': [{'name': c.name, 'pk': c.pk}
                        for c in obj.city_set.all()]
        }


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    name = serializers.CharField(required=False)
    region = serializers.CharField(source='region.name', required=False)
    country = serializers.CharField(source='country.name', required=False)

    class Meta:
        model = City
        fields = ('pk', 'name', 'region', 'country')


class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(queryset=Division.objects.all())
    name = serializers.CharField(required=False)
    number = serializers.CharField(required=False)

    class Meta:
        model = Division
        fields = ('pk', 'url', 'name', 'number',)


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

        data = validated_data.get('division', None)
        if data:
            instance.division = data['pk']
        data = validated_data.get('city', None)
        if data:
            instance.city = data['pk']
            instance.country = data['pk'].country
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
