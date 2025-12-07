from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM, create_access_token
from src.app.auth.schemas import UserCreate, UserSchema
from src.app.models import User
from src.core.security import verify_password, hash_password, decode_token, create_refresh_token
from src.app.database import get_session


async def login_service(form_data, session: AsyncSession):
    stmt = select(User).where(User.username == form_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    user.refresh_token = refresh_token
    session.add(user)
    await session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


async def refresh_token_service(data, session: AsyncSession):
    try:
        payload = decode_token(data.refresh_token)
        user_id = int(payload.get("sub"))
        if not user_id:
            raise HTTPException(401, "Invalid refresh token")
    except Exception:
        raise HTTPException(401, "Invalid refresh token")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user or user.refresh_token != data.refresh_token:
        raise HTTPException(401, "Refresh token expired or invalid")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    user.refresh_token = refresh_token
    session.add(user)
    await session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    statement = select(User).where(User.id == user_id)
    user = await session.execute(statement)
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def register_service(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session),
):
    statement = select(User).where(User.username == user_data.username)
    user = await session.execute(statement)
    user = user.fetchone()
    if user:
        raise HTTPException(400, "User already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role_id=user_data.role_id,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"message": "User created successfully"}


async def logout_service(current_user: UserSchema = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session)):
    statement = update(User).where(User.username == current_user.username).values(refresh_token=None)
    await session.execute(statement)
    await session.commit()
    return {"message": "User logged out"}
