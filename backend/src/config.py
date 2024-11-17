from functools import lru_cache
from schemas import MongoSettings, Settings


@lru_cache
def get_settings() -> Settings:
    return Settings(mongodb=MongoSettings())
