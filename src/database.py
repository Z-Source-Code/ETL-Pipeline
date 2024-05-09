import os
from supabase import create_client, Client

def create_sb_client():
  url: str = os.environ.get("SUPABASE_PROJECT_URL")
  key: str = os.environ.get("SUPABASE_API_KEY")
  supabase: Client = create_client(url, key)
  return supabase
