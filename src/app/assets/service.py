from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.assets.schemas import AssetSchema
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
        statement = select(Assets).where(Assets.secid == asset_secid.upper())
        result = await session.execute(statement)
        return result.scalars().one_or_none()

    @staticmethod
    async def create_asset_service(asset_info: AssetSchema, session: AsyncSession):
        asset = Assets(**asset_info.dict())
        session.add(asset)
        await session.commit()
        return asset

    @staticmethod
    async def delete_asset_service(asset_id: int, session: AsyncSession):
        statement = delete(Assets).where(Assets.id == asset_id)
        await session.execute(statement)
        await session.commit()
        return 200

    @staticmethod
    async def update_asset_service(asset_info: AssetSchema, session: AsyncSession):
        asset = Assets(**asset_info.dict())
        session.add(asset)
        await session.commit()
        return 200