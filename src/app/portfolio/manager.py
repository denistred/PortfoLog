from contextlib import asynccontextmanager

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import UserAssets, Events, EventType, Assets

class PortfolioManager:
    def __init__(self, user_id: int, session: AsyncSession):
        self.user_id = user_id
        self.session = session

    @asynccontextmanager
    async def transaction(self):
        try:
            yield self
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def buy(self, asset_id: int, portfolio_id: int, quantity: int):
        '''Функция для добавления актива в портфолио
            Изменяет UserAssets
            Изменяет Events
        '''
        statement = select(Assets).where(Assets.id == asset_id)
        result_asset = await self.session.execute(statement)
        asset = result_asset.scalar_one_or_none()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")


        stmt_asset = select(Assets).where(Assets.id == asset_id)
        result_asset = await self.session.execute(stmt_asset)
        asset = result_asset.scalar_one()
        price = asset.price

        user_asset = UserAssets(
            bought_price=price,
            portfolio_id=portfolio_id,
            quantity=quantity,
            asset_id=asset_id,
        )
        self.session.add(user_asset)
        await self.session.commit()


        stmt_event_type = select(EventType).where(EventType.name == "buy")
        result_event_type = await self.session.execute(stmt_event_type)
        event_type = result_event_type.scalar_one()

        event = Events(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            type_id=event_type.id,
            value=price * quantity
        )
        self.session.add(event)
        await self.session.commit()

        return user_asset, event

    async def sell(self, asset_id: int, portfolio_id: int, quantity: int):
        '''Функция для удаления актива из портфолио
            Изменяет UserAssets
            Изменяет Events
        '''
        statement = select(Assets).where(Assets.id == asset_id)
        result_asset = await self.session.execute(statement)
        asset = result_asset.scalar_one()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")

        stmt_asset = select(Assets).where(Assets.id == asset_id)
        result_asset = await self.session.execute(stmt_asset)
        asset = result_asset.scalar_one()
        price = asset.price

        statement = select(UserAssets).where(UserAssets.portfolio_id == portfolio_id,
                                             UserAssets.asset_id == asset_id)
        result_user_assets = await self.session.execute(statement)
        user_assets = result_user_assets.scalars().all()

        if not user_assets:
            raise HTTPException(status_code=404, detail="No assets to sell")

        remaining_quantity = quantity
        for user_asset in user_assets:
            if remaining_quantity <= 0:
                break

            if user_asset.quantity > remaining_quantity:
                user_asset.quantity -= remaining_quantity
                sold_quantity = remaining_quantity
                remaining_quantity = 0
            else:
                sold_quantity = user_asset.quantity
                remaining_quantity -= user_asset.quantity
                await self.session.delete(user_asset)


            statement_event_type = select(EventType).where(EventType.name == "sell")
            result_event_type = await self.session.execute(statement_event_type)
            event_type = result_event_type.scalar_one()

            event = Events(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                type_id=event_type.id,
                value=price * sold_quantity,
            )
            self.session.add(event)

        if remaining_quantity > 0:
            raise HTTPException(status_code=404, detail="Not enough quantity to sell")

        await self.session.commit()