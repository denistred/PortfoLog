from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int
    refresh_token: str

class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    class Config:
        extra = "forbid"


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
