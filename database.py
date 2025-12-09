from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client, Client

def conectar() -> Client:
    url: str = os.environ.get("SUPABASE_DB") # type: ignore
    key: str = os.environ.get("SUPABASE_KEY") # type: ignore

    if not url or not key:
        raise Exception("Error: Verifique los parametros de conexión")

    return create_client(url, key)
