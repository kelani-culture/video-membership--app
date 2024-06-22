import uuid

from cassandra.cqlengine import columns  # type: ignore
from cassandra.cqlengine.models import Model  # type: ignore

from app.config import get_settings
from . import security
from . import validators

settings = get_settings()


class User(Model):
    __keyspace__ = settings.astradb_keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)

        if q.count() != 0:
            raise Exception("User already has an account")
        valid, msg, email = validators.custom_validate_email(email)
        if not valid:
            raise Exception("Invalid email:", msg)
        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj

    def set_password(self, pw, commit=False):
        set_pwd = security.SecurePassword()
        self.password = set_pwd.generate_hash(pw)

        if commit:
            self.save()
        return True

    def verify_password(self, pw):
        pw_hash = self.password
        sec = security.SecurePassword()
        verified, _ = sec.confirm_password(pw_hash, pw)
        return verified

    def __repr__(self):
        return f"User {self.email}"
