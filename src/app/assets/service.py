from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Assets

class AssetService:
    @staticmethod
    async def get_all_assets(session: AsyncSession):
        statement = select(Assets)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_assets_by_id(asset_id: int, session: AsyncSession):
        statement = select(Assets).where(Assets.id == asset_id)
        result = await session.execute(statement)
        return result.scalars().one_or_none()

    @staticmethod
    async def get_assets_by_secid(asset_secid: str, session: AsyncSession):
        statement = select(Assets).where(Assets.secid == asset_secid)
        result = await session.execute(statement)
        return result.scalars().one_or_none()