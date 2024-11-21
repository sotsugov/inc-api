from typing import List, Optional
from pydantic import BaseModel


class UsageItem(BaseModel):
    message_id: int
    timestamp: str
    report_name: Optional[str] = None
    credits_used: float


class UsageResponse(BaseModel):
    usage: List[UsageItem]
