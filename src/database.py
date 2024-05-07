import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_API_KEY")
supabase: Client = create_client(url, key)

response = supabase.table('Job Postings').select("job_title").execute()

