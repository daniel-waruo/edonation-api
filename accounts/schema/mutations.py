import graphene

from accounts.schema.types import UserType
from accounts.serializers import (
    LoginSerializer,
    CreateAdminUserSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    ProfileSerializer
)
from accounts.serializers.password import PasswordChangeSerializer
from utils import Error, errors_to_graphene


class LoginMutation(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)
    errors = graphene.List(Error)

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        serializer = LoginSerializer(
            data=kwargs,
            context={
                'request': info.context
            }
        )
        if not serializer.is_valid():
            return LoginMutation(
                errors=errors_to_graphene(serializer.errors)
            )
        token, user = serializer.save()
        return LoginMutation(
            token=token,
            user=user
        )


class CreateAdminUserMutation(graphene.Mutation):
    """ create an administrative user of the system
    """
    user = graphene.Field(UserType)
    errors = graphene.List(Error)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated or not user.is_staff:
            return None
        serializer = CreateAdminUserSerializer(
            data=kwargs,
            context={
                "request": info.context
            }
        )
        if not serializer.is_valid():
            return CreateAdminUserMutation(
                errors=errors_to_graphene(serializer.errors)
            )
        return CreateAdminUserMutation(
            user=serializer.save()
        )


class EditUserProfileMutation(graphene.Mutation):
    """ changes user profile
    Args:
        user - user that has been changed
        errors - it is a list of errors to be return to the user
    """
    user = graphene.Field(UserType)
    errors = graphene.List(Error)

    class Arguments:
        """Define the data to be sent from the client
        Args:
            first_name - new first name of the user
            last_name  - last name of the user
        """
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        """ update the first name and last name of the user """
        # get request object
        request = info.context
        user = request.user
        if user.is_authenticated or not user.is_superuser:
            serializer = ProfileSerializer(
                data=kwargs
            )
            if serializer.is_valid():
                return EditUserProfileMutation(
                    user=serializer.save(user)
                )
            return EditUserProfileMutation(
                errors=errors_to_graphene(serializer.errors)
            )
        return EditUserProfileMutation(errors={
            Error(
                field='non_field_errors',
                errors=['User is Not Authenticated or Authorised']
            )
        })


class ResetPasswordMutation(graphene.Mutation):
    """Reset password"""
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        serializer = PasswordResetSerializer(
            data=kwargs,
            context={
                "request": info.context
            }
        )
        if serializer.is_valid():
            serializer.save()
            return ResetPasswordMutation(
                success=True
            )
        return ResetPasswordMutation(
            errors=errors_to_graphene(serializer.errors["email"])
        )


class ChangePasswordMutation(graphene.Mutation):
    """change the password of the current user"""
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        old_password = graphene.String()
        new_password1 = graphene.String()
        new_password2 = graphene.String()

    def mutate(self, info, **kwargs):
        serializer = PasswordChangeSerializer(
            data=kwargs,
            context={
                "request": info.context
            }
        )
        if serializer.is_valid():
            serializer.save()
            return ChangePasswordMutation(
                success=True
            )
        return ChangePasswordMutation(
            errors=errors_to_graphene(serializer.errors)
        )


class RegisterUserMutation(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(Error)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        serializer = RegisterSerializer(
            data=kwargs,
            context={
                "request": info.context
            }
        )
        if not serializer.is_valid():
            return RegisterUserMutation(
                errors=errors_to_graphene(serializer.errors)
            )
        serializer.save(request=info.context)
        return RegisterUserMutation(
            success=True
        )


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    register = RegisterUserMutation.Field()
    create_admin_user = CreateAdminUserMutation.Field()
    edit_user_profile = EditUserProfileMutation.Field()
    reset_password = ResetPasswordMutation.Field()
    change_password = ChangePasswordMutation.Field()
