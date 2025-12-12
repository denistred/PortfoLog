from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.user_assets.service import UserAssetsService
from src.app.user_assets.schemas import UserSchema
from src.app.auth.service import get_current_user
from src.app.database import get_session

router = APIRouter(prefix="/user_assets", tags=["user_assets"])


@router.get("/assets")
async def get_assets(
        portfolio_id: int,
        current_user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await UserAssetsService.get_assets(portfolio_id, current_user, session)


@router.post("/assets")
async def add_assets(
        asset_id: int,
        quantity: int,
        portfolio_id: int,
        user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await UserAssetsService.add_assets(asset_id, quantity, portfolio_id, user.id, session)