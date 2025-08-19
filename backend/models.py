from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    type: str  # "user" or "ai"
    content: str
    category: str  # "code", "analysis", "text"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    message: str
    category: str = "text"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    response: str
    category: str
    timestamp: datetime
    session_id: str

class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessage]