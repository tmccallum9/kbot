import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

assert SUPABASE_URL and SUPABASE_KEY, "Missing Supabase env vars!" # for local dev to check env vars

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def store_summary_to_supabase(user_id: str, raw_text: str, summary: str):
    supabase_client.table("summaries").insert({
        "user_id": user_id,
        "raw_message": raw_text,
        "summary": summary
    }).execute()
