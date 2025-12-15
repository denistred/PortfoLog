from sqlalchemy.ext.asyncio import AsyncSession
from src.app.portfolio.service import PortfolioService
from src.app.user_assets.service import UserAssetsService
from src.app.ui.schemas import UserSchema

class UserInterfaceService:
    @staticmethod
    async def get_portfolio_service(session: AsyncSession, current_user: UserSchema):
        user_portfolios = await PortfolioService.get_portfolios(current_user, session)
        if not user_portfolios:
            return []

        first_user_portfolios = user_portfolios[0].id
        user_assets = await UserAssetsService.get_assets(first_user_portfolios, current_user, session)

        return user_assets

