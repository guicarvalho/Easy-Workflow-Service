# coding: utf-8

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^users/$', views.UserProfileList.as_view(), name='user.list'),
    url(r'^users/(?P<username>\w+)/$', views.UserProfileDetail.as_view(), name='user.detail'),

    url(r'^requests/$', views.RequestList.as_view(), name='request.list'),

    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='token_auth'),
)