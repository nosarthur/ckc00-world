from rest_framework import serializers

from api.models import MyUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Model -> JSON
    """

    class Meta:
        model = MyUser
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'employer',)


class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    pass
