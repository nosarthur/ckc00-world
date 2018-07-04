from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    gender = serializers.BooleanField(source='ckcer.gender')
    phone = serializers.BooleanField(source='ckcer.phone')

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone',)
