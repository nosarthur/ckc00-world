from rest_framework import serializers

from api.models import MyUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    gender = serializers.BooleanField(source='ckcer.gender')
    phone = serializers.CharField(source='ckcer.phone')
    company = serializers.CharField(source='ckcer.company')

    class Meta:
        model = MyUser
        fields = ('url', 'email', 'first_name', 'last_name',
                  'gender', 'phone', 'company',)
