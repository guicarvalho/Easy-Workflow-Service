# coding: utf-8

from django.http.response import Http404

from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile, Request
from .serializers import UserProfileSerializer, RequestSerializer


class UserProfileList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, username):
        try:
            user = UserProfile.objects.filter(username=username).first()
            return user
        except UserProfile.DoesNotExists:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserProfileSerializer(user, data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)

        return Response(serializer.data)