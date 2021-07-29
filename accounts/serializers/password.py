from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm
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


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = False
        self.logout_on_password_change = False
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            err_msg = "Your old password was entered incorrectly. Please enter it again."
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
