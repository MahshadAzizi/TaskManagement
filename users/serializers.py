from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)
        token['phone_number'] = user.phone_number
        token['password'] = user.password
        return token


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        refresh_token = validated_data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']
