from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.service import get_current_user
from src.app.database import get_session
from src.app.events.schemas import UserSchema
from src.app.events.service import EventsService
from src.app.models import Events

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
async def get_events(portfolio_id: int,
                    current_user: UserSchema = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):

    result = await EventsService.get_events_service(1, current_user, session)
    return result