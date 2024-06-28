import os
import pathlib
from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"


os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    astradb_keyspace: Optional[str] = ''
    secret_key: Optional[str] = ''


@lru_cache
def get_settings():
    return DatabaseSettings()


if __name__ == "__main__":
    db_settings = get_settings()
    print(db_settings.model_dump())
