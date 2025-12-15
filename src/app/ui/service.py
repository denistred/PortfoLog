from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.models import UserAssets, Assets, Portfolios
from src.app.portfolio.service import PortfolioService
from src.app.ui.schemas import UserSchema
from src.app.models import Watchlists

class UserInterfaceService:
    @staticmethod
    async def get_portfolio_service(session: AsyncSession, current_user: UserSchema):
        statement_user_portfolios = select(Portfolios.id).where(Portfolios.user_id == current_user.id)
        user_portfolios = await session.execute(statement_user_portfolios)
        first_user_portfolio = user_portfolios.scalar_one_or_none()
        stmt = (
            select(UserAssets)
            .where(UserAssets.portfolio_id == first_user_portfolio)
            .options(selectinload(UserAssets.asset))
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items

    @staticmethod
    async def get_watchlist_service(session: AsyncSession, current_user: UserSchema):
        statement = select(Watchlists).where(Watchlists.user_id == current_user.id)
        result = await session.execute(statement)
        items = result.scalars().all()
        return items