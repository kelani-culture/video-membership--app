from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from app.shortcut import render, redirect
from app.users.decorators import login_required
from app import utils
from .schemas import VideoCreateSchema

router = APIRouter(
    prefix='/videos'
)


@router.get("/")
def video_list_view(request: Request):
    return render(request, "videos/list.html")

@router.get("/detail")
def video_detail_view(request: Request):
    return render(request, "videos/detail.html", {})


@router.get('/create', response_class=HTMLResponse)
@login_required
def video_get_create_view(request: Request):
    return render(request, "videos/create_video.html")


@router.post('/create', response_class=HTMLResponse)
@login_required
def video_post_create_view(request: Request, url: str = Form(...)):
    raw_data = {
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, VideoCreateSchema)
    context = {
        "data": data,
        "errors": errors,
        "url": url
    }
    if len(errors) > 0:
        return render(request, "videos/create_video.html",context,status_code=400)

    redirect_path = data.video_obj.get('path') or "/videos/create"
    return redirect(redirect_path)