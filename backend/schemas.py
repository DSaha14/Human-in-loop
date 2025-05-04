from pydantic import BaseModel

class HelpRequest(BaseModel):
    id: str
    question: str
    status: str  # 'pending', 'resolved', 'unresolved'
    answer: str | None = None

class AnswerSubmission(BaseModel):
    answer: str
