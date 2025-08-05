import os
from typing import Optional

# Only initialize the client in non-test environments
supabase_client: Optional[any] = None
if os.getenv("ENV") != "test":
    from supabase import create_client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


def store_summary_to_supabase(user_id: str, raw_text: str, summary: str):
    """
    Stores the summary in Supabase unless in test mode (ENV=test).
    """
    if os.getenv("ENV") == "test":
        print("[MOCKED] store_summary_to_supabase called")
        return

    if supabase_client is None:
        raise RuntimeError("Supabase client is not initialized")

    return supabase_client.table("summaries").insert({
        "user_id": user_id,
        "raw_message": raw_text,
        "summary": summary
    }).execute()
