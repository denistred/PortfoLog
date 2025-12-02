import asyncio

import requests
from sqlalchemy import select, update
from src.app.models import Assets
from src.app.database import async_session


class MOEXPriceUpdater:
    MOEX_URL = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"

    def fetch_prices(self):
        resp = requests.get(self.MOEX_URL)
        resp.raise_for_status()
        data = resp.json()
        return data

    def parse_prices(self, data):
        columns = data['securities']['columns']
        rows = data['securities']['data']

        idx_secid = columns.index('SECID')
        idx_price = columns.index('PREVLEGALCLOSEPRICE')

        price_map = {}
        for row in rows:
            secid = row[idx_secid]
            price = row[idx_price] or 0.0
            price_map[secid] = price

        return price_map

    async def update_prices(self):
        data = self.fetch_prices()
        prices = self.parse_prices(data)

        async with async_session() as session:
            for secid, price in prices.items():
                stmt = (
                    update(Assets)
                    .where(Assets.secid == secid)
                    .values(price=price)
                )
                await session.execute(stmt)

            await session.commit()

        print("Цены обновлены")

if __name__ == "__main__":
    updater = MOEXPriceUpdater()
    asyncio.run(updater.update_prices())