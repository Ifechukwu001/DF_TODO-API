from dj_rest_auth.views import LoginView as DJLoginView


class LoginAPIView(DJLoginView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    """

    pass
