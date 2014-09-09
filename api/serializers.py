# coding: utf-8

from .models import Request, UserProfile

from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'protocol', 'fone_number', 'cel_number', 'is_active', )


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('description', 'date', 'equipment', 'nature', 'status', 'priority', 'who_requested', 'who_executed',)