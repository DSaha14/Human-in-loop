import os
import time
import jwt
import requests
from dotenv import load_dotenv
from livekit import api

# Load environment variables
load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "").rstrip("/")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Validate environment setup
if not LIVEKIT_URL or not API_KEY or not API_SECRET:
    raise EnvironmentError("LIVEKIT_URL, API_KEY, or API_SECRET not set in .env")

def generate_jwt():
    now = int(time.time())
    payload = {
        "iss": API_KEY,
        "iat": now,
        "exp": now + 3600,
        "video": {
            "roomCreate": True,
            "roomList": True,
            "roomRecord": True,
            "roomAdmin": True
        }
    }

    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")

def safe_json_response(response):
    try:
        return response.json()
    except ValueError:
        print(f"❌ Invalid JSON response. Status: {response.status_code}, Raw content: {response.text}")
        return None

def create_room():
    room_name = "help-request-room"
    list_url = f"{LIVEKIT_URL}/admin/rooms"
    create_url = f"{LIVEKIT_URL}/admin/rooms"
    headers = {
        "Authorization": f"Bearer {generate_jwt()}",
        "Content-Type": "application/json"
    }

    # Step 1: List rooms
    list_response = requests.get(list_url, headers=headers)
    if list_response.status_code == 200:
        try:
            existing_rooms = list_response.json()
        except ValueError:
            print(f"⚠️ List rooms response not JSON. Raw content: {list_response.text}")
            existing_rooms = []
        for room in existing_rooms:
            if room.get("name") == room_name:
                print("ℹ️ Room already exists.")
                return {"sid": room.get("sid", room_name)}  # fallback to name if SID missing
    else:
        print(f"⚠️ Failed to list rooms. Status: {list_response.status_code}, Content: {list_response.text}")

    # Step 2: Create room
    data = {
        "name": room_name,
        "emptyTimeout": 300,
        "maxParticipants": 10
    }

    create_response = requests.post(create_url, headers=headers, json=data)
    if create_response.status_code == 200:
        try:
            return create_response.json()
        except ValueError:
            print("✅ Room created but no JSON returned. Assuming success.")
            return {"sid": room_name}
    else:
        print(f"❌ Failed to create room. Status: {create_response.status_code}, Content: {create_response.text}")
        return None


def add_participant(room_sid, participant_identity):
    url = f"{LIVEKIT_URL}/admin/rooms/{room_sid}/participants"
    headers = {
        "Authorization": f"Bearer {generate_jwt()}",
        "Content-Type": "application/json"
    }
    data = {
        "identity": participant_identity
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Participant '{participant_identity}' added successfully!")
        return safe_json_response(response)
    else:
        print(f"❌ Failed to add participant. Status: {response.status_code}, Content: {response.text}")
        return None

def send_message_to_room(room_sid, message):
    url = f"{LIVEKIT_URL}/admin/rooms/{room_sid}/message"
    headers = {
        "Authorization": f"Bearer {generate_jwt()}",
        "Content-Type": "application/json"
    }
    data = {
        "message": message
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"📩 Message sent to room {room_sid}: {message}")
        return safe_json_response(response)
    else:
        print(f"❌ Failed to send message. Status: {response.status_code}, Content: {response.text}")
        return None

def create_access_token(identity: str, room: str) -> str:
    """
    Generates a JWT access token for a given identity and room.
    """
    token = api.AccessToken() \
        .with_identity(identity) \
        .with_name(identity) \
        .with_grants(api.VideoGrants(room_join=True, room=room)) \
        .to_jwt()
    return token

# Example usage
if __name__ == "__main__":
    token = create_access_token("supervisor", "help-request-room")
    print("Generated Access Token:", token)
