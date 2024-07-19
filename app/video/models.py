
import uuid

from cassandra.cqlengine import columns  # type: ignore
from cassandra.cqlengine.models import Model  # type: ignore
from app.users.model import User
from app.config import get_settings
from .extractor import extract_video_id
from app.users.exceptions import InvalidUserIDException
from .exceptions import InvalidVideoURLException, VideoAddedException
settings = get_settings()


class Video(Model):
    __keyspace__ = "video_membership_app"
    host_id = columns.Text(primary_key=True) 
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()


    def __repr__(self):
        return f"title: {self.title}, url: {self.host_id}"

    @staticmethod
    def add_video(url, title, user_id=None):
        host_id = extract_video_id(url)
        if not host_id:
            raise InvalidVideoURLException('Invalid Youtube Video URL')
        user_exists = User.check_exist(user_id)

        if not user_exists:
            raise InvalidUserIDException('Invalid user_id')

        q = Video.objects.filter(host_id=host_id, user_id=user_id).allow_filtering()
        if q.count() != 0:
            raise VideoAddedException("Video already added")

        return Video.create(host_id=host_id, user_id=user_id, url=url, title=title)

    def as_data(self):
        return {f"{self.host_service}_id":  self.host_id, "path": self.path}

    @property
    def path(self):
        return f"/videos/{self.host_id}"