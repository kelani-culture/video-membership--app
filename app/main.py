import json
import pathlib

from cassandra.cqlengine.management import sync_table  # type: ignore
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from . import db, utils
from .shortcut import redirect, render
from .users.backends import JWTCookieBackend
from .users.decorators import login_required
from .users.exceptions import LoginRequiredException
from .users.model import User
from .users.schemas import UserLogInSchema, UserSignupSchema
from .video.models import Video
from .video.routers import router
# from .handlers import http_exception_handler
# Initialize the client

main_app = FastAPI()
video_router = router
main_app.include_router(video_router)

DB_SESSION = None


main_app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())


@main_app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "errors/main.html"
    context = {"status_code": status_code}
    return render(request, template_name, context, status_code)


@main_app.exception_handler(LoginRequiredException)
async def http_login_exception_handler(request, exc):
    return redirect(f"/login?next={request.url}", remove_session=True)


# DB on startup
@main_app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)


@main_app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {})
    context = {"abc": "abc"}
    return render(request, "home.html", context)


@main_app.get("/account", response_class=HTMLResponse)
@login_required
def account(request: Request):
    context = {}
    return render(request, "home.html", context)


@main_app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    # logged_in = request.cookies.get("session_id") is not None
    return render(request, "auth/login.html")


@main_app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    raw_data = {"email": email, "password": password}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLogInSchema)
    if len(errors) > 0:
        return render(request, "auth/login.html", raw_data, status_code=400)

    return redirect("/account", cookies=data.session_id)


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
    _ = data.pop("confirm_password")
    user_obj = User.create_user(**data)
    if len(errors) > 0:
        return render(request, "auth/login.html", raw_data, status_code=400)
    return redirect("/login")


@main_app.get("/users")
def user_list():
    q = User.objects.all()
    return list(q)
