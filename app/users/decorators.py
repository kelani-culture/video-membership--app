from functools import wraps

from fastapi import Request

from .auth import verify_user_token
from .exceptions import LoginRequiredException


def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        session_id = request.cookies.get("session_id")

        user_session = verify_user_token(session_id)
        if not user_session:
            raise LoginRequiredException(status_code=401)
        return func(request, *args, **kwargs)

    return wrapper
