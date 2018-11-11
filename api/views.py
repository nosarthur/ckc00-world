from typing import Union
from django.http import JsonResponse
from django.db.models import Count, Model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from cities_light.models import Country, Region

from api.permissions import IsSelfOrStaff
from api.serializers import (
    UserSerializer, PasswordSerializer, DivisionSerializer,
    CountrySerializer, RegionSerializer
    )
from api.models import MyUser, Division, Tag


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

    @action(methods=['patch'], detail=True)
    def set_password(self, request, pk=None):
        # /api/users/{id}/set_password/
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return JsonResponse({'status': 'false', 'message': ['Wrong password.']},
                                status=status.HTTP_403_FORBIDDEN)
            # set_password also hashes the password
            user.set_password(serializer.data['new_password'])
            user.save()
            return JsonResponse({'status': 'password set'})

        return JsonResponse({'status': 'false', 'message': serializer.errors},
                            status=status.HTTP_403_FORBIDDEN)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This access point returns the name of the countries in the database and
    the regions in each country.

    /api/country/{id}/
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This access point returns the name of the regions in the database and
    the cities in each country.

    /api/region/{id}/
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.GenericViewSet):
    """
    This is used to delete tag from user
    """
    permission_classes = (IsSelfOrStaff,)
    queryset = Tag.objects.all()
#    serializer_class = TagSerializer

    def destroy(self, request, pk):
        """
        delete all tags is not supported
        """
        u = request.user
        try:
            t = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return JsonResponse({'staus': 'false', 'message': 'tag does not exist.'})
        u.tags.remove(t)
        return JsonResponse({'status': 'tag removed'})


class CountryMapViewSet(viewsets.GenericViewSet):
    """
    This is for map view
    """
    # FIXME: authenticated only?
    permission_classes = [permissions.AllowAny]

    # @action(methods=['get'], detail=True)
    # def get(self, request):
    def retrieve(self, request, pk=None):
        # TODO: return user data
        #       fullname and url
        #       maybe a new user serializer
        return


class GenderViewSet(viewsets.GenericViewSet):

    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False)
    def tags(self, request):
        # tag view /api/gender/tags/?name=&number=
        division_name = request.GET.get('name', None)
        division_number = request.GET.get('number', None)
        return _make_gender_JsonResponse(Tag,
            division_name, division_number)

    @action(methods=['get'], detail=False)
    def countries(self, request):
        # country view /api/gender/countries/?name=&number=
        division_name = request.GET.get('name', None)
        division_number = request.GET.get('number', None)
        return _make_gender_JsonResponse(Country,
            division_name, division_number)


def _make_gender_JsonResponse(
    model: Model,
    division_name: Union[str, None],
    division_number: Union[str, None],
    limit=10) -> JsonResponse:
    """
    Query the user table with optional division name and number parameters,
    return a JsonResponse with the gender statistics for eachmodel instance.
    The Json format is as follows
        {
            [o1.name, [n_female1, n_male1]],
            [o2.name, [n_female2, n_male2]],
            ...
        }
    where o is a row of the model.
    """
    # FIXME: magic number
    maxCount = 6
    objs = model.objects.annotate(num_users=Count('myuser')).order_by('-num_users')[:maxCount]
    result = []
    kwargs = {}
    if division_name is not None:
        kwargs = {'division__name': division_name}
        if division_number is not None:
            kwargs['division__number'] = division_number

    for o in objs:
        users = o.myuser_set.filter(**kwargs)
        n_total = len(users)
        n_female = users.filter(gender='f').count()
        result.append([o.name, [n_female, n_total - n_female]])
    return JsonResponse(result, safe=False)


class DivisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Division means Class
    """
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [permissions.AllowAny]
