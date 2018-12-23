from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'gender', views.GenderViewSet, base_name='gender')
router.register(r'divisions', views.DivisionViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feedback/', csrf_exempt(views.feedback), name='feedback')
]
