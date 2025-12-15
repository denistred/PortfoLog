from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.service import get_current_user
from src.app.database import get_session
from src.app.watchlist.service import WatchlistService
from src.app.watchlist.schemas import UserSchema

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/")
async def get_watchlists(current_user: UserSchema = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    result = await WatchlistService.get_watchlist_service(session, current_user)
    return result

@router.post("/")
async def add_to_watchlist(asset_id: int,
                           current_user: UserSchema = Depends(get_current_user),
                           session: AsyncSession = Depends(get_session)):
    result = await WatchlistService.add_to_watchlist_service(asset_id, session, current_user)
    return result

@router.delete("/")
async def remove_from_watchlist(asset_id: int,
                                current_user: UserSchema = Depends(get_current_user),
                                session: AsyncSession = Depends(get_session)):
    result = await WatchlistService.delete_from_watchlist_service(asset_id, session, current_user)
    return result
