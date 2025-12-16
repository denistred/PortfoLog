import aiohttp
import asyncio
from datetime import datetime
from influxdb_client import Point
from src.app.quotes.influxdb_client import write_api
from src.core.config import INFLUXDB_BUCKET

BASE_SECURITIES_URL = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
HISTORY_URL_TEMPLATE = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json"

MAX_CONCURRENT_REQUESTS = 5


async def fetch_tickers(session: aiohttp.ClientSession):
    async with session.get(BASE_SECURITIES_URL) as resp:
        data = await resp.json()
        columns = data['securities']['columns']
        secid_idx = columns.index('SECID')
        tickers = [row[secid_idx] for row in data['securities']['data']]
        return tickers


async def fetch_and_save_history(session: aiohttp.ClientSession, ticker: str, semaphore: asyncio.Semaphore, start: str = None, end: str = None):
    async with semaphore:
        params = {}
        if start:
            params['from'] = start
        if end:
            params['till'] = end

        url = HISTORY_URL_TEMPLATE.format(ticker=ticker)
        try:
            async with session.get(url, params=params, timeout=10) as resp:
                data = await resp.json()
                columns = data['history']['columns']
                for row in data['history']['data']:
                    date_str = row[columns.index('TRADEDATE')]
                    open_price = row[columns.index('OPEN')]
                    high_price = row[columns.index('HIGH')]
                    low_price = row[columns.index('LOW')]
                    close_price = row[columns.index('CLOSE')]
                    volume = row[columns.index('VOLUME')]

                    if date_str is None or close_price is None:
                        continue

                    point = (
                        Point("stock_prices")
                        .tag("ticker", ticker)
                        .field("open", float(open_price))
                        .field("high", float(high_price))
                        .field("low", float(low_price))
                        .field("close", float(close_price))
                        .field("volume", float(volume))
                        .time(datetime.strptime(date_str, "%Y-%m-%d"))
                    )
                    write_api.write(bucket=INFLUXDB_BUCKET, record=point)

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            await asyncio.sleep(1)


async def main():
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tickers = await fetch_tickers(session)
        print(f"Found {len(tickers)} tickers, e.g. {tickers[:5]}")

        tasks = [fetch_and_save_history(session, ticker, semaphore, start="2024-01-01", end="2025-12-14") for ticker in tickers]
        await asyncio.gather(*tasks)
        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
