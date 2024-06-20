import pathlib

from cassandra.cqlengine.management import sync_table  # type: ignore
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from . import db
from .users.model import User

# Initialize the client

main_app = FastAPI()


DB_SESSION = None


BASE_DIR = pathlib.Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


# DB on startup
@main_app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@main_app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "abc": 123}
    )


@main_app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@main_app.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    print(email, password)
    return templates.TemplateResponse("auth/login.html", {"request": request})


@main_app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@main_app.post("/signup", response_class=HTMLResponse)
def signup_post(
    request: Request, email: str = Form(...), password: str = Form(...),
    password_confirm: str = Form(...)
):
    print(email, password)
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@main_app.get("/users")
def user_list():
    q = User.objects.all()
    return list(q)
