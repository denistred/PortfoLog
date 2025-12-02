from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Assets


class AssetsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_assets(self):
        statement = select(Assets)
        result = await self.session.execute(statement)
        assets = result.scalars().all()
        return assets