from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.schemas import TokenSchema
from src.app.auth.service import login_service, get_current_user, register_service
from src.app.auth.schemas import UserSchema, UserCreate
from src.app.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
async def login_route(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    return await login_service(form_data, session)


@router.get("/me")
async def read_me_route(current_user: UserSchema = Depends(get_current_user)):
    return {"username": current_user.username}


@router.post("/register")
async def register_route(
        user_data: UserCreate,
        result=Depends(register_service)
):
    return await register_service(user_data, result)
