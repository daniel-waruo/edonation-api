import graphene
from graphene.utils.str_converters import to_camel_case


class Error(graphene.ObjectType):
    """ represent errors
        field - field for which the error is called
        messages - messages in the field
    """
    field = graphene.String()
    messages = graphene.List(graphene.String)


def errors_to_graphene(errors: dict):
    """Changes Serialization Errors to My Graphene Error Type
    Args:
        errors - errors from a serializer
    """
    graphene_errors = []
    # create a list of Error Objects
    for error in errors.keys():
        graphene_errors.append(
            Error(
                field=to_camel_case(error),
                messages=errors[error]
            )
        )
    return graphene_errors
