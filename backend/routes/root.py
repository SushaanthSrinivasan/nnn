from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from backend.db.db_operations import get_profiles, get_all_profiles,get_conversations, suggest_messages
from backend.db.databases import create_supabase_client

router = APIRouter()
supabase = create_supabase_client()

@router.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app"}

@router.get("/profiles/{search_term}")
def search_profiles(search_term: str):
    data = get_profiles(supabase, search_term)
    if data.data:
        return JSONResponse(content=data.data, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="No profiles found")
    return {"search_term": search_term}

@router.get("/profiles")
def search_profiles():
    data = get_all_profiles(supabase)
    if data.data:
        return JSONResponse(content=data.data, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="No profiles found")
    return {"search_term": search_term}

@router.get("/conversations/{person_id}")
def search_conversations(person_id: str):
    data = get_conversations(supabase, person_id)
    if data.data:
        return JSONResponse(content=data.data, media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="No conversations found")

# @router.get("/suggest-messages/{person_id}")
# def recommend_messages(request: Request, person_id: str, message: str):
#     body = await request.json()
#     content = body.get("content")
#     sender_id = body.get("sender_id")

@router.post("/suggest-messages/{person_id}")
async def recommend_messages(request: Request, person_id: str):
    body = await request.json()  # Retrieve the JSON body
    message = body.get("message")  # Get the message from the body
    # return {"person_id": person_id, "message": message}

    print(f'person_id: {person_id}\nmessage: {message}')

    response = suggest_messages(supabase, person_id, message)
    print(response.content[0].text)

    text_response = response.content[0].text
    return JSONResponse(content=text_response, media_type="application/json")