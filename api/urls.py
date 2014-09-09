# coding: utf-8

from django.conf.urls import patterns, include, url

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserProfileViewSet)
router.register(r'requests', views.RequestViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls),),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='token_auth'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)