from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class SecurePassword:
    def generate_hash(self, pw_raw):
        ph = PasswordHasher()
        return ph.hash(pw_raw)

    def confirm_password(self, hash_pwd, pw_raw):
        ph = PasswordHasher
        verified = False
        msg = ''

        try:
            verified = ph.verify(hash_pwd, pw_raw) 
        except VerifyMismatchError:
            verify = False
            msg = 'Invalid password.'
        except Exception as e:
            verified = False
            msg = f'Unexpected Error: \n{e}'

        return verified, msg