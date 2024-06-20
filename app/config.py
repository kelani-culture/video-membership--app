from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import os


os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8')
    astradb_keyspace: str = ''


@lru_cache
def get_settings() -> DatabaseSettings:
    return DatabaseSettings()


if __name__ == '__main__':
    db_settings = get_settings()
    print(db_settings.model_dump())