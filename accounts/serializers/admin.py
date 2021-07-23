from rest_framework import serializers

from accounts.models import User


class CreateAdminUserSerializer(serializers.Serializer):
    """ DRF Serializer responsible for creating new users on the admin page

    This class is responsible for creating the user and sending him an email containing their
    password

    """

    first_name = serializers.CharField(
        max_length=255,
        min_length=1,
        required=True
    )
    last_name = serializers.CharField(
        max_length=255,
        min_length=1,
        required=True
    )
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, value):
        if User.objects.filter(phone=value):
            raise serializers.ValidationError("Phone number must be unique")
        return value

    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email must be unique")
        return value

    def save(self, **kwargs):
        user = User.objects.create_admin_user(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            phone=self.validated_data["phone"],
            email=self.validated_data["email"],
            creator=self.context["request"].user
        )
        return user
