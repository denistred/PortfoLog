import csv
import io
from fastapi import HTTPException
from sqlalchemy import select, delete

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

    @staticmethod
    async def delete_portfolio_service(portfolio_id: int, current_user: UserSchema, session: AsyncSession):
        statement = select(Portfolios).where(Portfolios.user_id == current_user.id)
        result = await session.execute(statement)
        portfolios = result.scalars().all()

        if not portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        if portfolio_id not in [x.id for x in portfolios]:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        statement = delete(Portfolios).where(Portfolios.id == portfolio_id)
        await session.execute(statement)
        await session.commit()
        return {"status": "ok"}

    @staticmethod
    def to_csv(items: list[dict]) -> io.StringIO:
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Asset ID",
            "Name",
            "SECID",
            "Quantity",
            "Avg Price",
            "Current Price",
        ])

        for item in items:
            writer.writerow([
                item["id"],
                item["name"],
                item["secid"],
                item["quantity"],
                round(item["avg_price"], 2),
                round(item["current_price"], 2),
            ])

        output.seek(0)
        return output