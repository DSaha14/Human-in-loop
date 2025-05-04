from uuid import uuid4
from .database import load_data, save_data

def get_pending_requests():
    data = load_data()
    return [req for req in data["requests"] if req["status"] == "pending"]

def save_answer(request_id, answer):
    data = load_data()
    for req in data["requests"]:
        if req["id"] == request_id:
            req["status"] = "resolved"
            req["answer"] = answer
            data["knowledge"].append({"question": req["question"], "answer": answer})
            break
    save_data(data)

def get_knowledge_base():
    return load_data()["knowledge"]

def create_help_request(question):
    data = load_data()
    request = {
        "id": str(uuid4()),
        "question": question,
        "status": "pending",
        "answer": None
    }
    data["requests"].append(request)
    save_data(data)
    return request
