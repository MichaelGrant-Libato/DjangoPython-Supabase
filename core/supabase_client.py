import os
from supabase import create_client, Client

# Use SERVICE key for server-side operations that need elevated perms;
# fall back to ANON for basic calls.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase URL/KEY missing. Check your .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()
