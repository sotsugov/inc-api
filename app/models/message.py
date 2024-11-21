from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    timestamp: datetime
    id: int
    report_id: Optional[int] = None


class Messages(BaseModel):
    messages: List[Message]
