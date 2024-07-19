from typing import Any, Dict

from cassandra.cqlengine.query import DoesNotExist, MultipleObjectsReturned
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import BASE_DIR, TEMPLATE_DIR

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def redirect(path, cookies: dict = {}, remove_session=False):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)

    if remove_session:
        response.set_cookie(key="session_ended", value=1)
        response.delete_cookie("session_id")
    return response


def render(
    request: Request,
    template_name: str,
    context: Dict[str, Any] = {},
    status_code: int = 200,
    cookies: Dict[str, Any] = {},
):
    ctx = context.copy()
    ctx.update({"request": request})

    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    if cookies:
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)
    # #delete cookies
    # for key in request.cookies.keys():
    #     response.delete_cookie(key)
    return response


def get_object_or_404(KlassName, **kwargs):
    obj = None
    try:
        obj = KlassName.objects.get(**kwargs)
    except DoesNotExist:
        raise StarletteHTTPException(status_code=404)
    except MultipleObjectsReturned:
        obj = KlassName.objects.allow_filter().filter(**kwargs)
        return obj.first()
        # StarletteHTTPException(status_code=400)
    except:
        raise StarletteHTTPException(status_code=500)
    return obj
