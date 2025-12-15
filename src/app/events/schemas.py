from datetime import datetime

from pydantic import BaseModel, EmailStr


class EventSchema(BaseModel):
    id: int
    portfolio_id: int
    type_id: int
    asset_id: int
    created_at: datetime
    value: float

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    role_id: int
