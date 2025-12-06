from contextlib import asynccontextmanager
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
from src.app.database import get_session, engine, Base
from src.app.service import AssetsService
from src.app.auth.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get("/assets")
async def get_all_assets(session: AsyncSession = Depends(get_session)):
    service = AssetsService(session)
    assets = await service.get_all_assets()
    return assets
