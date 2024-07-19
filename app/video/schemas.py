from pydantic import BaseModel, field_validator, model_validator
import uuid
from app.users.exceptions import InvalidUserIDException
from typing import Optional
from .exceptions import InvalidVideoURLException, VideoAddedException
from .extractor import extract_video_id
from .models import Video


class VideoCreateSchema(BaseModel):
    url: str  # user generated
    user_id: uuid.UUID  # request.session user_id
    video_obj: Optional[dict] = None
    title: str

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, v, values, **kwrgs):
        url = v
        video_id = extract_video_id(url)

        if video_id is None:
            raise ValueError(f"{url} is not a valid youtube url")
        return url

    @model_validator(mode="after")
    def validate_data(self):
        url = self.url
        user_id = self.user_id
        video_obj = None
        title = self.title
        try:
            video_obj = Video.add_video(url, user_id=user_id, title=title)
        except InvalidUserIDException:
            raise ValueError("Invalid User ID provided")
        except InvalidVideoURLException:
            raise ValueError("Invalid Youtube video URL provided.")
        except VideoAddedException:
            raise ValueError("Video already existed")
        except Exception as e:
            raise ValueError(e)
        if video_obj is None:
            raise ValueError("There's a problem with your account")
        if not isinstance(video_obj, Video):
            raise ValueError("There's a problem with your account")

        self.video_obj = video_obj.as_data()

        return self.video_obj