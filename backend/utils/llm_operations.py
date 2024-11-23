import anthropic
from dotenv import load_dotenv
import os

load_dotenv('./backend/.env')

ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")



def recommend_messages(person_profile, last_3_conversations, message):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.0,
        system="You are a conversation analyst assistant.",
        messages=[
            {"role": "user", "content": f"You will be given 3 inputs, a persons profile, previous coversations with the person and their current message. Suggest a reply message to send to them. Only return the message, no other text. \n\nPerson's profile: {person_profile}\n\nPrevious conversations: {last_3_conversations}\n\nCurrent message: {message}"}
        ]
    )
    # print(response)
    return response

def suggest_starter_message(person_profile, last_3_conversations):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.0,
        system="You are a conversation analyst assistant.",
        messages=[
            {"role": "user", "content": f"You will be given 2 inputs, a persons profile and previous coversations with the person. Suggest a starting message to send to them. Only return the message, no other text. \n\nPerson's profile: {person_profile}\n\nPrevious conversations: {last_3_conversations}\n\nCurrent message: {message}"}
        ]
    )
    # print(response)
    return response