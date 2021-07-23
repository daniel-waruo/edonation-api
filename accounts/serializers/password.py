from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.forms import PasswordResetForm
from accounts.models import User


class ChangePasswordSerializer(serializers.ModelSerializer):
    """ DRF serializer that changes the password of a particular User"""

    class Meta:
        model = User
        fields = ['password']

    def create(self, validated_data):
        User.objects.get(
            username=validated_data["username"]
        ).set_password(validated_data["new_password"])

    def validate(self, data):
        user = authenticate(
            **{
                "username": data["username"],
                "password": data["current_password"],
            }
        )
        if not user or not user.is_active:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, )

    def validate(self, attrs):
        self.form = PasswordResetForm(attrs)
        if not self.form.is_valid():
            raise serializers.ValidationError(detail=self.form.errors)
        return attrs

    def save(self, **kwargs):
        self.form.save()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
