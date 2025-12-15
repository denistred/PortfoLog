from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.watchlist.schemas import UserSchema
from src.app.models import Watchlists


class WatchlistService:
    @staticmethod
    async def get_watchlist_service(session: AsyncSession, current_user: UserSchema):
        statement = select(Watchlists).where(Watchlists.user_id == current_user.id)
        result = await session.execute(statement)
        items = result.scalars().all()
        return items

    @staticmethod
    async def add_to_watchlist_service(asset_id: int, session: AsyncSession, current_user: UserSchema):
        statement = select(Watchlists).where(Watchlists.user_id == current_user.id)
        result = await session.execute(statement)
        item = result.scalars().all()
        if asset_id in [x.asset_id for x in item]:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Asset ID already exists")
        new_watchlist = Watchlists(asset_id=asset_id, user_id=current_user.id)
        session.add(new_watchlist)
        await session.commit()
        return {"status": "ok"}

    @staticmethod
    async def delete_from_watchlist_service(asset_id: int, session: AsyncSession, current_user: UserSchema):
        statement = delete(Watchlists).where(Watchlists.user_id == current_user.id, Watchlists.asset_id == asset_id)
        result = await session.execute(statement)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found in watchlist"
            )
        return {"status": "ok"}
