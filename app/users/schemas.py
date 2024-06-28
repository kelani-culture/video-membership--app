from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    model_validator,
)

from . import auth
from .model import User


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("email")
    @classmethod
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError("Email is not available")
        return v

    @model_validator(mode="after")
    def password_match(self):
        if self.confirm_password != self.password:
            raise ValueError("confirm password must be the same as password")
        return self


class UserLogInSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: Optional[str] = None

    @model_validator(mode="after")
    def validate_user(self):
        error_msg = "Incorrect credential please try again."
        email = self.email or None
        password = self.password or None

        if email is None or password is None:
            raise ValueError(error_msg)
        password = password.get_secret_value()
        user_obj = auth.authenticate(email, password)
        if user_obj is None:
            raise ValueError(error_msg)

        token = auth.login(user_obj)
        self.session_id = token
        #return {"session_id": token}
