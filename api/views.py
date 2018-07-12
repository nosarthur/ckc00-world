from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from api.permissions import IsOwnerOrReadOnly
from api.serializers import UserSerializer
from api.models import MyUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = (permissions.IsAdminUser, )
        elif self.action in ('update', 'partial_update'):
            permission_classes = (IsOwnerOrReadOnly,)
        else:
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny])
    def division(self):
        pass


class DivisionViewSet(viewsets.ModelViewSet):
    pass
