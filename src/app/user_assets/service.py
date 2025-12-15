from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.models import Assets, UserAssets, Portfolios
from src.app.user_assets.schemas import UserSchema

from src.app.portfolio.manager import PortfolioManager

class UserAssetsService:
    @staticmethod
    async def get_assets(portfolio_id: int, user: UserSchema, session: AsyncSession):
        statement = select(Portfolios.id).where(Portfolios.user_id == user.id)
        user_portfolios = await session.execute(statement)
        user_portfolios = [row[0] for row in user_portfolios.all()]
        if portfolio_id not in user_portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        statement = select(UserAssets).where(UserAssets.portfolio_id == portfolio_id).options(selectinload(UserAssets.asset))
        result = await session.execute(statement)
        user_assets = result.scalars().all()
        return user_assets


    @staticmethod
    async def add_assets(asset_id: int, quantity: int, portfolio_id: int, user_id: int, session: AsyncSession):
        manager = PortfolioManager(user_id, session)
        await manager.buy(asset_id, portfolio_id, quantity)
        return 200

    @staticmethod
    async def remove_assets(asset_id: int, quantity: int, portfolio_id: int, user_id: int, session: AsyncSession):
        manager = PortfolioManager(user_id, session)
        await manager.sell(asset_id, quantity, portfolio_id)
        return 200