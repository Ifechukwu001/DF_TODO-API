from functools import lru_cache
from pathlib import Path
from decouple import Config, RepositoryEnv, config as decouple_config

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


@lru_cache()
def get_config() -> Config:
    if ENV_FILE.exists():
        return Config(RepositoryEnv(ENV_FILE))
    return decouple_config


config = get_config()
