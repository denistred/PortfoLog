from pydantic import BaseModel

class AssetSchema(BaseModel):
        id: int
        name: str
        secid: str
        asset_type: int
        price: float
        currency_id: int
