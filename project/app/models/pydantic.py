from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int

class UserPayloadSchema(BaseModel):
    email: str
    password_hash: str