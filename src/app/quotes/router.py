from fastapi import APIRouter

from src.app.quotes.service import QuotesService

router = APIRouter(prefix="/quotes", tags=["quotes"])

@router.get("/{secid}")
async def get_quote(secid: str):
    prices = await QuotesService.get_prices_by_secid_service(secid)
    return {"secid": secid, "price": prices}