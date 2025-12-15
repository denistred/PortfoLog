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
        new_watchlist = Watchlists(asset_id=asset_id, user_id=current_user.id)
        session.add(new_watchlist)
        await session.commit()
        return 200

    @staticmethod
    async def delete_from_watchlist_service(asset_id: int, session: AsyncSession, current_user: UserSchema):
        statement = delete(Watchlists).where(Watchlists.user_id == current_user.id, Watchlists.asset_id == asset_id)
        await session.execute(statement)
        await session.commit()
        return 200