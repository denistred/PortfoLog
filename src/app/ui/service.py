from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.models import UserAssets, Assets
from src.app.portfolio.service import PortfolioService
from src.app.ui.schemas import UserSchema


class UserInterfaceService:
    @staticmethod
    async def get_portfolio_service(session: AsyncSession, current_user: UserSchema):

        stmt = (
            select(UserAssets)
            .where(UserAssets.portfolio_id == 1)
            .options(selectinload(UserAssets.asset))
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items