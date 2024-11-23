from backend.utils.llm_operations import recommend_messages

def get_profiles(supabase, search_term):
    # print(f'search_term: {search_term}')
    formatted_search_term = f"{search_term.replace(' ', ':* | ')}:*"
    data = supabase.table("persons").select("*").text_search("name", formatted_search_term).execute()
    # data = supabase.table("persons").select("*").execute()
    # print(f'data: {data}')
    return data

def get_profile_by_id(supabase, person_id):
    # print(f'search_term: {search_term}')
    # formatted_search_term = f"{search_term.replace(' ', ':* | ')}:*"
    # data = supabase.table("persons").select("*").text_search("name", formatted_search_term).execute()
    data = supabase.table("persons").select("*").eq("id", person_id).execute()
    # data = supabase.table("persons").select("*").execute()
    # print(f'data: {data}')
    return data

def get_conversations(supabase, person_id, limit=3):
    # data = supabase.table("conversations").select("*").eq("person_id", person_id).execute()
    data = supabase.table("conversations") \
        .select("*") \
        .eq("person_id", person_id) \
        .order("convo_timestamp", desc=True) \
        .limit(limit) \
        .execute()
    return data

def suggest_messages(supabase, person_id, message):
    last_3_conversations = get_conversations(supabase, person_id).data
    person_profile = get_profile_by_id(supabase, person_id).data
    response = recommend_messages(person_profile,last_3_conversations, message)
    return response
    

