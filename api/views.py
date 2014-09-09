# coding: utf-8

from rest_framework import viewsets, permissions

from .models import UserProfile, Request
from .serializers import UserProfileSerializer, RequestSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer