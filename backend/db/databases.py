from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv('./backend/.env')

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
SECRET = os.getenv("SUPABASE_SECRET")

# print(f'URL: {URL}\nKEY: {KEY}\nSECRET: {SECRET}')

def create_supabase_client():
    supabase: Client = create_client(URL, KEY)
    return supabase