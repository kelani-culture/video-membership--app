import datetime

from jose import ExpiredSignatureError, jwt
from  jose.exceptions import JWTError
from app import config

from .model import User

ALGORITHM = "HS256"
settings = config.get_settings()


def authenticate(email, password):
    user_obj = None
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password):
        return None

    return user_obj


def login(user_obj, expires=5):
    raw_data = {
        "user_id": str(user_obj.user_id),
        "role": "admin",
        "exp": datetime.datetime.now() + datetime.timedelta(seconds=expires),
    }
    return jwt.encode(raw_data, settings.secret_key, algorithm=ALGORITHM)


def verify_user_token(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except (ExpiredSignatureError, JWTError):
        pass
    if "user_id" not in data:
        return None
    return data
