from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app import utils
from app.shortcut import get_object_or_404, redirect, render
from app.users.decorators import login_required

from .models import Video
from .schemas import VideoCreateSchema

router = APIRouter(prefix="/videos")


@router.get("/")
def video_list_view(request: Request):
    q = Video.objects.all()
    context = {"object_list": q}
    return render(request, "videos/list.html", context=context)

@router.get("/{host_id}")
def video_detailed_view(request: Request, host_id: str):
    obj = get_object_or_404(Video, host_id=host_id)
    context = {"host_id": host_id, "object": obj}
    return render(request, "videos/detail.html", context=context)

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_get_create_view(request: Request):
    return render(request, "videos/create_video.html")


@router.post("/create", response_class=HTMLResponse)
@login_required
def video_post_create_view(
    request: Request, url: str = Form(...), title: str = Form(...)
):
    raw_data = {"title": title, "url": url, "user_id": request.user.username}
    print(raw_data)
    data, errors = utils.valid_schema_data_or_error(
        raw_data, VideoCreateSchema
    )
    context = {"data": data, "errors": errors, "url": url}
    if len(errors) > 0:
        return render(
            request, "videos/create_video.html", context, status_code=400
        )

    redirect_path = data.video_obj.get("path") or "/videos/create"
    return redirect(redirect_path)
