from fastapi import APIRouter, Depends
from src.app.user.schemas import UserSchema
from src.app.auth.service import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserSchema)
async def read_me_route(current_user: UserSchema = Depends(get_current_user)):
    return current_user