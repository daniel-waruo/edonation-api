import graphene

from accounts.schema.types import Error, errors_to_graphene, UserType
from accounts.serializers import LoginSerializer, CreateAdminUserSerializer


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

    def mutate(self, info, **kwargs):
        """ update the first name and last name of the user """
        # get request object
        request = info.context
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        user = request.user
        if user.is_authenticated:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return EditUserProfileMutation(
                user=user
            )
            # return errors in the serializer
        return EditUserProfileMutation(errors={
            Error(
                field='non_field_errors',
                errors=['User is Not Authenticated']
            )
        })


class Mutation(graphene.ObjectType):
    login = LoginMutation.Field()
    create_admin_user = CreateAdminUserMutation.Field()
    edit_user_profile = EditUserProfileMutation.Field()