from contextlib import asynccontextmanager
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, engine, Base
from fastapi import FastAPI




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan, title="FastAPI + PostgreSQL Example")
