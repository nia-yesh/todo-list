from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from apps.accounts.serializers import SignUpUserSerializer


class SignUpUserView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpUserSerializer
