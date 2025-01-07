from uuid import uuid4
from django.conf import settings


def get_session_id(request):
    session = request.session.get(settings.SESSION_IDENTIFIER, None)
    if session is None:
        session = uuid4().hex
        request.session[settings.SESSION_IDENTIFIER] = session
    return session
