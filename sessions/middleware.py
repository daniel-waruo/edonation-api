from uuid import uuid4, UUID


def is_valid_uuid4(string):
    try:
        uuid_obj = UUID(string, version=4)
    except ValueError:
        return False
    return uuid_obj.hex == string


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.method != "OPTIONS":
            # get your session key
            user_session = request.headers.get('user-session', "")
            print(f"session from headers {user_session}")
            if not user_session or not is_valid_uuid4(user_session):
                user_session = uuid4().hex
            print(f"session before {user_session}")
            request.user_session = user_session

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if request.method != "OPTIONS":
            user_session = request.user_session
            print(f"session after {user_session}")
            response["user-session"] = user_session
        return response
