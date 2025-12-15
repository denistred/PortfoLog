from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import get_session
from src.app.assets.service import AssetService
from src.app.assets.schemas import AssetSchema
from src.app.auth.service import require_role
from src.app.auth.schemas import UserSchema

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


@router.post("/", response_model=AssetSchema)
async def create_asset(asset_info: AssetSchema,
                       admin_user: UserSchema = Depends(require_role(2)),
                       session: AsyncSession = Depends(get_session)):
    return await AssetService.create_asset_service(asset_info, session)

@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, admin_user: UserSchema = Depends(require_role(2)), session: AsyncSession = Depends(get_session)):
    return await AssetService.delete_asset_service(asset_id, session)

@router.put("/{asset_id}")
async def update_asset(asset_id: int,
                        asset_info: AssetSchema,
                       admin_user: UserSchema = Depends(require_role(2)),
                       session: AsyncSession = Depends(get_session)):
    return await AssetService.update_asset_service(asset_info, session)
