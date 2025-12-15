from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.assets.service import AssetService
from src.app.portfolio.service import PortfolioService
from src.app.user_assets.service import UserAssetsService
from src.app.ui.schemas import UserSchema
from src.app.watchlist.service import WatchlistService
from src.app.models import Assets

class UserInterfaceService:
    @staticmethod
    async def get_portfolio_service(session: AsyncSession, current_user: UserSchema):
        user_portfolios = await PortfolioService.get_portfolios(current_user, session)
        if not user_portfolios:
            return []

        first_user_portfolios = user_portfolios[0].id
        user_assets = await UserAssetsService.get_assets(first_user_portfolios, current_user, session)

        joined_assets = {}
        for asset in user_assets:
            if asset.asset.id not in joined_assets:
                joined_assets[asset.asset.id] = {
                    "id": asset.asset.id,
                    "name": asset.asset.name,
                    "secid": asset.asset.secid,
                    "quantity": asset.quantity,
                    "current_price": asset.asset.price,
                    "avg_price": asset.bought_price,
                }
            else:
                prev = joined_assets[asset.asset.id]
                total_quantity = prev["quantity"] + asset.quantity
                prev["avg_price"] = (prev["avg_price"] * prev["quantity"] + asset.bought_price * asset.quantity) / total_quantity
                prev["quantity"] = total_quantity

        return list(joined_assets.values())

    @staticmethod
    async def get_watchlist_service(current_user: UserSchema, session: AsyncSession):
        watchlist_items = await WatchlistService.get_watchlist_service(
            session=session,
            current_user=current_user,
        )

        if not watchlist_items:
            return []

        asset_ids = [w.asset_id for w in watchlist_items]

        stmt = select(Assets).where(Assets.id.in_(asset_ids))
        result = await session.execute(stmt)
        assets = result.scalars().all()

        return assets
