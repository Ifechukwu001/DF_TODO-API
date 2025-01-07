from django.conf import settings


def get_session_id(request):
    return request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
