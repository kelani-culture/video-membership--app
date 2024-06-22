from typing import Any, Dict
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .config import BASE_DIR, TEMPLATE_DIR

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render(
    request: Request,
    template_name: str,
    context: Dict[str, Any] = {},
    status_code: int = 200,
    cookie: Dict[str, Any] = {}
):
    ctx = context.copy()
    ctx.update({"request": request})

    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    if not cookie:
        response.set_cookie(**cookie, httponly=True)
    return response
