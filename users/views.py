from rest_framework.permissions import IsAuthenticated
from customize.views import CustomViewSet, CustomJWTAuthenticationView
from users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer


class RegisterView(CustomViewSet):
    serializer_class = RegisterSerializer
    permission_classes = []
    allow_http_methods = ['post']


class LoginView(CustomJWTAuthenticationView):
    serializer_class = LoginSerializer
    allow_http_methods = ['post']


class LogoutView(CustomViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LogoutSerializer
    allow_http_methods = ['post']
