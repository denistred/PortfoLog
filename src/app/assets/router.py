from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import get_session
from src.app.assets.service import AssetService
from src.app.assets.schemas import AssetSchema

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=list[AssetSchema])
async def all_assets(
        session: AsyncSession = Depends(get_session)
):
    result = await AssetService.get_all_assets(session)
    return result

@router.get("/{asset_info}", response_model=AssetSchema)
async def get_asset_by_id_or_secid(asset_info: str, session: AsyncSession = Depends(get_session)):
    if asset_info.isdigit():
        return await AssetService.get_assets_by_id(int(asset_info), session)
    else:
        return await AssetService.get_assets_by_secid(asset_info, session)