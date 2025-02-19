import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.getenv("SUPABASE_URL", "postgres")
key = os.getenv("SUPABASE_KEY", "mysecretpassword")
client = create_client(url, key)


def get_supabase_client() -> Client:
    return client
