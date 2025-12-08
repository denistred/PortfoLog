from fastapi import HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.portfolio.schemas import UserSchema, CreatePortfolioSchema
from src.app.models import Portfolios, PortfolioTypes


class PortfolioService:
    @staticmethod
    async def get_portfolios(current_user: UserSchema, session: AsyncSession):
        statement = select(Portfolios).where(Portfolios.user_id == current_user.id)
        result = await session.execute(statement)
        portfolios = result.scalars().all()
        return portfolios

    @staticmethod
    async def create_portfolio(portfolio_data: CreatePortfolioSchema, current_user: UserSchema, session: AsyncSession):
        statement = select(PortfolioTypes).where(PortfolioTypes.id == portfolio_data.portfolio_type)
        portfolio_type = await session.execute(statement)
        if not portfolio_type:
            raise HTTPException(status_code=404, detail="Portfolio type not found")

        portfolio = Portfolios(
            name=portfolio_data.name,
            portfolio_type=portfolio_data.portfolio_type,
            user_id=current_user.id,
        )
        session.add(portfolio)
        await session.commit()
        return portfolio
