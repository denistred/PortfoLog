import asyncio
import requests
from src.app.models import Assets
from src.app.database import async_session

class MOEXLoader:
    asset_types = {
        "share": 1,
        "bond": 2,
    }

    currencies = {
        "SUR": 2,  # рубль
        "USD": 1,
    }

    MOEX_URL = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"

    def __init__(self):
        self.assets = []

    def fetch_data(self):
        resp = requests.get(self.MOEX_URL)
        resp.raise_for_status()
        data = resp.json()
        return data

    def initial_parse_assets(self, data):
        columns = data['securities']['columns']
        rows = data['securities']['data']

        idx_secid = columns.index('SECID')
        idx_name = columns.index('SECNAME')
        idx_currency = columns.index('CURRENCYID')
        idx_price = columns.index('PREVLEGALCLOSEPRICE')

        assets_list = []

        for row in rows:
            asset_type_id = self.asset_types["share"]
            currency_code = row[idx_currency]
            price = row[idx_price] or 0.0

            asset = Assets(
                name=row[idx_name],
                secid=row[idx_secid],
                asset_type=asset_type_id,
                price=price,
                currency_id=self.currencies.get(currency_code, self.currencies["SUR"])
            )
            assets_list.append(asset)

        self.assets = assets_list
        return assets_list

    async def save_assets(self):
        if not self.assets:
            print("Нет данных для сохранения")
            return

        async with async_session() as session:
            session.add_all(self.assets)
            await session.commit()
            print(f"Сохранено {len(self.assets)} активов")

    async def run(self):
        data = self.fetch_data()
        self.initial_parse_assets(data)
        await self.save_assets()


if __name__ == "__main__":
    loader = MOEXLoader()
    asyncio.run(loader.run())
