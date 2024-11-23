from fastapi import FastAPI
from .routes import items, root
from .db.databases import create_supabase_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]  # Add your frontend URL here

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(items.router)

# supabase = create_supabase_client()