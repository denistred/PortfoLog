from contextlib import asynccontextmanager
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from src.app.database import get_session, engine, Base
from src.app.assets.router import router as assets_router
from src.app.auth.auth import router as auth_router
from src.app.user.router import router as user_router


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


