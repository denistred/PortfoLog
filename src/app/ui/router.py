from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.auth.service import get_current_user
from src.app.database import get_session
from src.app.events.service import EventsService
from src.app.ui.schemas import UserSchema
from src.app.ui.service import UserInterfaceService
from src.app.auth.service import authenticate_user, create_access_token
from src.app.assets.service import AssetService
from src.app.watchlist.service import WatchlistService

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/portfolio", response_class=HTMLResponse)
async def get_portfolio(
        request: Request,
        current_user: UserSchema = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
        items = await UserInterfaceService.get_portfolio_service(session, current_user)
        return templates.TemplateResponse(
            "portfolio.html",
            {"request": request, "username": current_user.username, "title": "Портфель", "assets": items},
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(username, password, session)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    token = create_access_token({"sub": str(user.id)})

    response = RedirectResponse("/ui/portfolio", status_code=302)
    response.set_cookie("access_token", token)

    return response

@router.get("/watchlist", response_class=HTMLResponse)
async def watchlist_page(request: Request,
                         current_user: UserSchema = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    items = await WatchlistService.get_watchlist_service(session, current_user)
    return templates.TemplateResponse(
        "watchlist.html",
        {"request": request, "title": "Watchlist", "username": current_user.username, "watchlists": items},
    )

@router.get("/assets", response_class=HTMLResponse)
async def assets_page(request: Request,
                      session: AsyncSession = Depends(get_session)):
    items = await AssetService.get_all_assets(session)
    return templates.TemplateResponse(
        "stocks.html",
        {"request": request, "title": "Assets", "username": "","stocks": items},
    )

@router.get("/events", response_class=HTMLResponse)
async def events_page(request: Request,
                      current_user: UserSchema = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)):
    events = await EventsService.get_events_service(1, current_user, session)
    return templates.TemplateResponse(
        "events.html",
        {"request": request, "title": "Events", "username": current_user.username,"events": events},
    )