from django.contrib.auth.models import User

from rest_framework import viewsets
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
