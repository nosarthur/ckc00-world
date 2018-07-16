from rest_framework import serializers

from api.models import MyUser, Division, Tag


class DivisionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Division
        fields = ('url', 'name', 'number',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    division = DivisionSerializer(required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = MyUser
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'employer', 'homepage',
                  'division', 'tags')


class PasswordSerializer:
    pass
