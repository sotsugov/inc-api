from pydantic import BaseModel


class Report(BaseModel):
    id: int
    name: str
    credit_cost: int
