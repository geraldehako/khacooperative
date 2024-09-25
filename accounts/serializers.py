from rest_framework import serializers
from .models import Utilisateurs

class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField()
