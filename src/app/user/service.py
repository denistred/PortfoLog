from sqlalchemy import update, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.user.schemas import UserUpdateSchema, UserSchema
from src.app.models import User
from src.core.security import create_access_token, create_refresh_token


class UserService:
    @staticmethod
    async def update_user(current_user: UserSchema, update_data: UserUpdateSchema, session: AsyncSession):
        data = update_data.model_dump(exclude_none=True)

        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(**data)
            .returning(User)
        )
        result = await session.execute(stmt)
        await session.commit()

        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession):
        statement = Delete(User).where(User.id == user_id)
        result = await session.execute(statement)
        await session.commit()
        return {"message": "success"}