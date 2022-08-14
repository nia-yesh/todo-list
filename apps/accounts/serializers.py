from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from apps.accounts.models import User


class SignUpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=(validate_password,))

    class Meta:
        model = User
        fields = ("id", "username", "password", "role")

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                        role=validated_data['role'])
        return user
