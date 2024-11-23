from fastapi import FastAPI
from .routes import items, root
from .db.databases import create_supabase_client

app = FastAPI()

app.include_router(root.router)
app.include_router(items.router)

# supabase = create_supabase_client()