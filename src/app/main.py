from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.database import engine, Base
from src.app.assets.router import router as assets_router
from src.app.auth.auth import router as auth_router
from src.app.user.router import router as user_router
from src.app.portfolio.router import router as portfolio_router
from src.app.user_assets.router import router as user_assets_router
from src.app.ui.router import router as user_router_ui
from src.app.watchlist.router import router as watchlist_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(assets_router)
app.include_router(portfolio_router)
app.include_router(user_assets_router)
app.include_router(user_router_ui)
app.include_router(watchlist_router)