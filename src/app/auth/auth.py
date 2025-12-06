from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from src.app.auth.schemas import TokenSchema
from src.app.auth.service import login_service, get_current_user, register_service, refresh_token_service, logout_service
from src.app.auth.schemas import UserSchema, UserCreate, RefreshTokenSchema
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

@router.post("/refresh", response_model=TokenSchema)
async def refresh_route(
    data: RefreshTokenSchema,
    session: AsyncSession = Depends(get_session)
):
    return await refresh_token_service(data, session)

@router.post("/logout")
async def logout_route(
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await logout_service(current_user, session)