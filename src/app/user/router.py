from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.database import get_session
from src.app.user.schemas import UserSchema, UserUpdateSchema, TokenSchema
from src.app.auth.service import get_current_user
from src.app.user.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserSchema)
async def read_me_route(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserSchema)
async def patch_me_route(
        update_data: UserUpdateSchema,
        current_user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    updated = await UserService.update_user(current_user, update_data, session)
    return updated


@router.delete("/me")
async def delete_me_route(
        current_user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    deleted = await UserService.delete_user(current_user.id, session)
    return deleted
