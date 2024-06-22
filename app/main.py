import json
import pathlib

from cassandra.cqlengine.management import sync_table  # type: ignore
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse

from . import db, utils
from .shortcut import render
from .users.model import User
from .users.schemas import UserLogInSchema, UserSignupSchema

# Initialize the client

main_app = FastAPI()


DB_SESSION = None


# DB on startup
@main_app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@main_app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, "home.html", {"abc": 123})


@main_app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return render(request, "auth/login.html", {})


@main_app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    raw_data = {"email": email, "password": password}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLogInSchema)

    if len(errors) > 0:
        return render(request, "auth/login.html", raw_data, status_code=400)
    return render(request, "auth/login.html", {"data": data, "errors": errors})


@main_app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return render(request, "auth/signup.html", {})


@main_app.post("/signup", response_class=HTMLResponse)
def signup_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
):
    raw_data = {
        "email": email,
        "password": password,
        "confirm_password": password_confirm,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    if len(errors) > 0:
        return render(request, "auth/login.html", raw_data, status_code=400)
    return render(request, "auth/signup.html", {"data": data, "errors": error})


@main_app.get("/users")
def user_list():
    q = User.objects.all()
    return list(q)
