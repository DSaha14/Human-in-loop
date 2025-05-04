from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
import os
from dotenv import load_dotenv
from livekit_utils import create_room, add_participant, send_message_to_room

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HelpRequest(BaseModel):
    question: str

class AnswerRequest(BaseModel):
    answer: str

requests_db = []
logs = []
knowledge_base = {}

@app.post("/help")
def handle_help_request(req: HelpRequest):
    request_id = str(uuid.uuid4())[:8]
    print(f"Handling help request {request_id}...")

    log_event = lambda msg: logs.append({"request_id": request_id, "event": msg})
    log_event("🔔 New help request received")

    room = create_room()
    if not room:
        log_event("❌ Failed to create room")
        raise HTTPException(status_code=500, detail="Failed to create room")

    room_sid = room.get("sid")
    if not room_sid:
        log_event("❌ Room SID not found")
        raise HTTPException(status_code=500, detail="Room SID missing")

    add_participant(room_sid, "supervisor")
    log_event("✅ Supervisor added to room")

    message = f"Help needed for request {request_id}: '{req.question}'"
    send_message_to_room(room_sid, message)
    log_event(f"📩 Message sent: {message}")

    # Save to DB
    requests_db.append({
        "id": request_id,
        "question": req.question,
        "status": "pending",
        "room_sid": room_sid
    })

    log_event("📝 Request stored as pending")
    return {"request_id": request_id, "room_sid": room_sid}

@app.get("/logs")
def get_logs():
    return logs

@app.get("/requests")
def get_requests():
    return requests_db

@app.get("/knowledge")
def get_knowledge():
    return knowledge_base

@app.get("/get-token")
def get_token(identity: str = Query(...)):
    # Simulated token logic — replace with actual if needed
    return {"token": f"fake-token-for-{identity}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
