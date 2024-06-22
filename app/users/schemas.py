from pydantic import BaseModel, EmailStr, SecretStr, field_validator, model_validator

from .model import User


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator('email')
    @classmethod
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError('Email is not available')
        return v

    @model_validator(mode='after')
    def password_match(self):
        if self.confirm_password != self.password:
            raise ValueError('confirm password must be the same as password')
        return self

class UserLogInSchema(BaseModel):
    email: EmailStr
    password: SecretStr