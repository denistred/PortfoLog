from src.core.config import INFLUXDB_ORG, INFLUXDB_BUCKET
from src.app.quotes.influxdb_client import query_api

class QuotesService:
    @staticmethod
    async def get_prices_by_secid_service(secid: str):
        secid = secid.upper()
        query = f'''
            from(bucket:"{INFLUXDB_BUCKET}")
              |> range(start: 0)  // start: 0 означает всё время
              |> filter(fn: (r) => r._measurement == "stock_prices")
              |> filter(fn: (r) => r["ticker"] == "{secid}")
              |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
              |> sort(columns: ["_time"])
            '''

        tables = query_api.query(org=INFLUXDB_ORG, query=query)
        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    "time": record.get_time().isoformat(),
                    "open": record.values.get("open"),
                    "high": record.values.get("high"),
                    "low": record.values.get("low"),
                    "close": record.values.get("close"),
                    "volume": record.values.get("volume")
                })
        return results