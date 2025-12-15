from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.portfolio.service import PortfolioService
from src.app.events.schemas import UserSchema
from src.app.models import Events


class EventsService:
    @staticmethod
    async def get_events_service(portfolio_id: int, current_user: UserSchema, session: AsyncSession):
        user_portfolios = await PortfolioService.get_portfolios(current_user, session)
        if portfolio_id not in [x.id for x in user_portfolios]:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        statement = select(Events).where(Events.portfolio_id == portfolio_id)
        result = await session.execute(statement)
        events = result.scalars().all()
        return events
