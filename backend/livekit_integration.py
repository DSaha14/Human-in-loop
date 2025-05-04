import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def create_room():
    url = f"{LIVEKIT_URL}/admin/rooms"
    headers = {
        "Authorization": f"Bearer {API_SECRET}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "help-request-room",  # Room name
        "emptyTimeout": 300,  # Optional
        "maxParticipants": 10  # Optional
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Room created successfully!")
        return response.json()
    else:
        print(f"Failed to create room: {response.text}")
        return None

def add_participant(room_sid, participant_identity):
    url = f"{LIVEKIT_URL}/admin/rooms/{room_sid}/participants"
    headers = {
        "Authorization": f"Bearer {API_SECRET}",
        "Content-Type": "application/json"
    }
    data = {
        "identity": participant_identity
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Participant {participant_identity} added successfully!")
        return response.json()
    else:
        print(f"Failed to add participant: {response.text}")
        return None

def send_message_to_room(room_sid, message):
    url = f"{LIVEKIT_URL}/admin/rooms/{room_sid}/message"
    headers = {
        "Authorization": f"Bearer {API_SECRET}",
        "Content-Type": "application/json"
    }
    data = {
        "message": message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Message sent to room {room_sid}: {message}")
        return response.json()
    else:
        print(f"Failed to send message: {response.text}")
        return None

# Run the functions
room = create_room()
if room:
    room_sid = room['sid']
    add_participant(room_sid, "supervisor_identity")
    send_message_to_room(room_sid, "Need help with customer query!")
