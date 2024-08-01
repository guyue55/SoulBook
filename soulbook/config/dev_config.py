#!/usr/bin/env python
import os

from .config import Config


class DevConfig(Config):
    """
    Dev config for soulbook
    """

    VAL_HOST = os.getenv('VAL_HOST', 'false')

    # Database config
    REDIS_DICT = dict(
        IS_CACHE=True,
        REDIS_ENDPOINT=os.getenv('REDIS_ENDPOINT', "localhost"),
        REDIS_PORT=int(os.getenv('REDIS_PORT', 6379)),
        REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None),
        REDIS_PORT=6379,
        CACHE_DB=0,
        SESSION_DB=1,
        POOLSIZE=10,
    )
    MONGODB = dict(
        MONGO_HOST=os.getenv('MONGO_HOST', "127.0.0.1"),
        MONGO_PORT=int(os.getenv('MONGO_PORT', 27017)),
        MONGO_USERNAME="",
        MONGO_PASSWORD="",
        DATABASE='soulbook',
    )

    # website
    WEBSITE = dict(
        IS_RUNNING=os.getenv('OWLLOOK_IS_RUNNING', True),
        TOKEN=os.getenv('OWLLOOK_TOKEN', '')
    )

    AUTH = {
        "Owllook-Api-Key": os.getenv('OWLLOOK_API_KEY', "your key")
    }
