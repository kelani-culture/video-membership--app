from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    """
    Login Required Exception
    """


class InvalidUserIDException(Exception):
    """
    Invalid User ID exception
    """


class UserHasAccountException(Exception):
    """
    User already has an account exception
    """

class InvalidEmailException(Exception):
    """
    Invalid email exceptions
    """

