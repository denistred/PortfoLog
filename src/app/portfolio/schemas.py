from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int

class CreatePortfolioSchema(BaseModel):
    name: str
    portfolio_type: int