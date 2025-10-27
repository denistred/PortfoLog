from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# declarative base class
class Base(DeclarativeBase):
    pass


class Assets(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    asset_type: Mapped[int] = mapped_column(ForeignKey("assets_types.id"))
    price: Mapped[float] = mapped_column(nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"))


class AssetsTypes(Base):
    __tablename__ = "assets_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Currencies(Base):
    __tablename__ = "currencies"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    role_id: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Watchlists(Base):
    __tablename__ = "watchlists"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class EventType(Base):
    __tablename__ = "event_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Events(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("event_types.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    value: Mapped[float] = mapped_column()


class Portfolios(Base):
    __tablename__ = "portfolios"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    portfolio_type: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class UserAssets(Base):
    __tablename__ = "user_assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    bought_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    bought_price: Mapped[float] = mapped_column()
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    quantity: Mapped[int] = mapped_column()
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))


class DividendsTime(Base):
    __tablename__ = "dividends_time"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    value: Mapped[float] = mapped_column()
    paytime: Mapped[datetime] = mapped_column()


class Quotes(Base):
    __tablename__ = "quotes"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    price_open: Mapped[float] = mapped_column()
    price_close: Mapped[float] = mapped_column()
