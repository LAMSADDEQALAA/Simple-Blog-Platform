import os
from dotenv import load_dotenv
from aiocache import Cache
load_dotenv()

cache: Cache = Cache.from_url(os.getenv("REDIS_URL"))