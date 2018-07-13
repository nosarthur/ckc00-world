from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from api.permissions import IsSelfOrStaff
from api.serializers import UserSerializer, PasswordSerializer 
from api.models import MyUser, Division

INVALID_REQEUST = 'Not a valid request.'


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            permission_classes = (permissions.IsAdminUser, )
        elif self.action in ('update', 'partial_update', 'set_password'):
            permission_classes = (IsSelfOrStaff,)
        elif self.action in ('list', 'retrieve'):
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.AllowAny,)
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=True)
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return JsonResponse({'status': 'password set'})
        else:
            return JsonResponse({'status': 'false', 'message': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def gender(self, request):
        # filter, this is for gender view
        dname = request.GET.get('name', None)
        cname = request.GET.get('country', None)
        if dname is None and cname is None:
            users = MyUser.objects.all()
            return _make_gender_JsonResponse(users)
        if dname is not None and cname is not None:
            return JsonResponse({'status': 'false', 'message': INVALID_REQEUST},
                status=status.HTTP_400_BAD_REQUEST)
        if dname is not None:
            kwargs = {'division__name': dname}
            num = request.GET.get('number')
            if num is not None:
                kwargs['division__number'] = num
            users = MyUser.objects.filter(**kwargs)
            return _make_gender_JsonResponse(users)
        # TODO: country

    @action(methods=['get'], detail=False)
    def country(self, request):
        # filter, this is for map view
        pass


def _make_gender_JsonResponse(users):
    """
    :type users: queryset
    """
    n_total = len(users)
    n_male = users.filter(gender='M').count()
    return JsonResponse({'M': n_male, 'F': n_total - n_male})


class DivisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Division means Class
    """
    queryset = Division.objects.all()
    serializer_class = 0  # TODO
    permission_classes = [permissions.AllowAny]

