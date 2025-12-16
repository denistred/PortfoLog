from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.app.database import engine, Base
from src.app.assets.router import router as assets_router
from src.app.auth.auth import router as auth_router
from src.app.user.router import router as user_router
from src.app.portfolio.router import router as portfolio_router
from src.app.user_assets.router import router as user_assets_router
from src.app.ui.router import router as user_router_ui
from src.app.watchlist.router import router as watchlist_router
from src.app.events.router import router as event_router
from src.app.quotes.router import router as quotes_router

from src.parser.moex_updater import main as update_prices
from src.core.backup import DatabaseBackupService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(update_prices, 'interval', minutes=1)
    scheduler.add_job(
        DatabaseBackupService.backup_and_upload,
        trigger="cron",
        hour=3,
        minute=0,
    )
    scheduler.start()

    yield

    await engine.dispose()
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
scheduler = AsyncIOScheduler()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(assets_router)
app.include_router(portfolio_router)
app.include_router(user_assets_router)
app.include_router(user_router_ui)
app.include_router(watchlist_router)
app.include_router(event_router)
app.include_router(quotes_router)