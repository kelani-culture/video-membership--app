from . import auth
from fastapi import Request
from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)



class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        session_id = request.cookies.get("session_id")
        user_data = None
        if session_id:
            user_data= auth.verify_user_token(session_id)
        if user_data is None:
            roles = ['annon']
            return AuthCredentials(roles), UnauthenticatedUser()
        user_id = user_data.get('user_id')
        roles = ['authenticated']
        return AuthCredentials(roles), SimpleUser(user_id)