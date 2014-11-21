# coding: utf-8

from django.http.response import Http404
from django.shortcuts import get_object_or_404

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
            # serializer.save()

            # TODO: improve implementation in serializer
            UserProfile.objects.create_user(
                username=request.DATA.get('username'),
                password=request.DATA.get('password'), 
                email=request.DATA.get('email'), 
                role=request.DATA.get('role'), 
                first_name=request.DATA.get('first_name'), 
                last_name=request.DATA.get('last_name'), 
                protocol=request.DATA.get('protocol'), 
                fone_number=request.DATA.get('fone_number'),
                cel_number=request.DATA.get('cel_number'), 
                is_active=True
            )

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

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestListByUser(APIView):

    REALIZED_STATUS = 'realized'
    PENDIND_STATUS = 'pending'
    DELAYED_STATUS = 'delayed'
    CANCELED_STATUS = 'canceled'

    def get_object(self, username):
        user = get_object_or_404(UserProfile, username=username)

        if not user:
            raise Http404

        requests_of_user = Request.objects.filter(who_executed=user.id).all()
        return requests_of_user

    def get(self, request, username, format=None):
        requests_of_user = self.get_object(username)
        serializer = RequestSerializer(requests_of_user)

        realized_tasks = 0
        pending_tasks = 0
        delayed_tasks = 0
        canceled_tasks = 0

        for r in requests_of_user:
            
            if r.status == self.REALIZED_STATUS:
                realized_tasks += 1
            
            elif r.status == self.PENDIND_STATUS:
                pending_tasks += 1
            
            elif r.status == self.DELAYED_STATUS:
                delayed_tasks += 1
            
            elif r.status == self.CANCELED_STATUS:
                canceled_tasks += 1

        total_of_tasks = {
            'realized': realized_tasks,
            'pending': pending_tasks,
            'delayed': delayed_tasks,
            'canceled': canceled_tasks,
        }

        return Response(total_of_tasks)


class RequestListByStatus(APIView):
    
    def get_object(self, username, status):
        user = get_object_or_404(UserProfile, username=username)

        if not user:
            raise Http404

        requests_of_user = Request.objects.filter(who_executed=user.id, status=status).all()
        return requests_of_user

    def get(self, request, username, status, format=None):
        requests_of_user = self.get_object(username, status)

        serializer = RequestSerializer(requests_of_user)

        return Response(serializer.data)


class RequestListAllByUser(APIView):

    def get_object(self, username):
        try:
            user = UserProfile.objects.filter(username=username).first()
            requests_of_user = Request.objects.filter(who_executed=user.id).all()
            return requests_of_user

        except UserProfile.DoesNotExists:
            raise Http404

    def get(self, request, username, format=None):
        requests_of_user = self.get_object(username)
        serializer = RequestSerializer(requests_of_user)

        return Response(serializer.data)
