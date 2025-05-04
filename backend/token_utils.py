import os
import time
import jwt

def generate_join_token(room_name, identity):
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    now = int(time.time())
    payload = {
        "iss": API_KEY,
        "sub": identity,
        "iat": now,
        "exp": now + 3600,
        "room": room_name,
        "video": {
            "roomJoin": True
        }
    }

    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return token if isinstance(token, str) else token.decode("utf-8")
