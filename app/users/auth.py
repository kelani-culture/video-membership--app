from .model import User
from jose import ExpiredSignatureError, jwt
import datetime
from app import config


ALGORITHM = 'HS256'
settings = config.get_settings()


def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password):
        return None

    return user_obj

def login(user_obj, expires=5):
    raw_data = {"user_id": str(user_obj.user_id), "role": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=5)}
    return jwt.encode(raw_data, settings.secret_key, algorithm=ALGORITHM)


def verify_user_token(token):
    verify = False
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        verify = True
    except ExpiredSignatureError:
        verify = False
        pass

    if 'user_id' not in data:
        return None
    return data, verify