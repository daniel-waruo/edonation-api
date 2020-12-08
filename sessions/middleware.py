from uuid import uuid4

from django.utils.deprecation import MiddlewareMixin

SESSION_COOKIE_NAME = "USER_SESSION"


class UserSessionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # get your session key
        user_session = request.COOKIES.get(SESSION_COOKIE_NAME)
        if 'user-session' in request.headers:
            user_session = request.headers['user-session']
        if not user_session:
            user_session = str(uuid4())
        request.user_session = user_session

    def process_response(self, request, response):
        user_session = request.user_session
        if not user_session:
            user_session = str(uuid4())
        response["user-session"] = user_session
        return response
