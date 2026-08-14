import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")