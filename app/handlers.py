# from starlette.exceptions import HTTPException
# from .main import main_app
# from .shortcut import render

# @main_app.exception_handler
# async def http_exception_handler(request, exc):
#     status_code = exc.status_code
#     template_name = "errors/main.html"
#     context = {"status_code": status_code}
#     return render(request, template_name, context, status_code)

