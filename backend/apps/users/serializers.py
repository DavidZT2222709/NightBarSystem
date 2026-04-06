from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")
        return user
    
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']