import uuid

import graphene


class CreateAnonymousSession(graphene.Mutation):
    session_key = graphene.String()

    def mutate(self, info, product_id, quantity):
        return CreateAnonymousSession(
            session=uuid.uuid4()
        )


class Mutation(graphene.ObjectType):
    create_session = CreateAnonymousSession.Field()
