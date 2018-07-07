from rest_framework import viewsets, permissions
# from api.permissions import IsOwnerOrReadOnly
from api.serializers import UserSerializer
from api.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          )
