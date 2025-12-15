from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.portfolio.service import PortfolioService
from src.app.portfolio.schemas import UserSchema, CreatePortfolioSchema
from src.app.auth.service import get_current_user
from src.app.database import get_session

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/portfolio")
async def get_portfolios(
    current_user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await PortfolioService.get_portfolios(current_user, session)

@router.post("/portfolio")
async def create_portfolio(
        portfolio: CreatePortfolioSchema,
        current_user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await PortfolioService.create_portfolio(portfolio, current_user, session)

@router.delete("/portfolio/{portfolio_id}")
async def delete_portfolio(portfolio_id: int, current_user: UserSchema = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await PortfolioService.delete_portfolio_service(portfolio_id, current_user, session)