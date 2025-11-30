import os
import logging
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)

class SupabaseConnection:
    __instance = None
    __client: Client | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SupabaseConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url:
                raise Exception("SUPABASE_URL missing")
            if not key:
                raise Exception("SUPABASE_KEY missing")

            try:
                self.__class__.__client = create_client(url, key)
                logger.info("Supabase connection created successfully")
            except Exception as e:
                logger.exception("Failed to create Supabase client")
                raise e

    @classmethod
    def get_client(cls) -> Client:
        if cls.__client is None:
            cls()
        return cls.__client
