from django.conf.urls import url, include

from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='myuser')
router.register(r'classes', views.DivisionViewSet, base_name='division')

urlpatterns = [
    url(r'^', include(router.urls)),
]
