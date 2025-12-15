import csv
import io
from fastapi import HTTPException
from sqlalchemy import select, delete
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.portfolio.schemas import UserSchema, CreatePortfolioSchema
from src.app.models import Portfolios, PortfolioTypes


class PortfolioService:
    @staticmethod
    async def get_portfolios(current_user: UserSchema, session: AsyncSession):
        statement = select(Portfolios).where(Portfolios.user_id == current_user.id)
        result = await session.execute(statement)
        portfolios = result.scalars().all()
        return portfolios

    @staticmethod
    async def create_portfolio(portfolio_data: CreatePortfolioSchema, current_user: UserSchema, session: AsyncSession):
        statement = select(PortfolioTypes).where(PortfolioTypes.id == portfolio_data.portfolio_type)
        portfolio_type = await session.execute(statement)
        if not portfolio_type:
            raise HTTPException(status_code=404, detail="Portfolio type not found")

        portfolio = Portfolios(
            name=portfolio_data.name,
            portfolio_type=portfolio_data.portfolio_type,
            user_id=current_user.id,
        )
        session.add(portfolio)
        await session.commit()
        return portfolio

    @staticmethod
    async def delete_portfolio_service(portfolio_id: int, current_user: UserSchema, session: AsyncSession):
        statement = select(Portfolios).where(Portfolios.user_id == current_user.id)
        result = await session.execute(statement)
        portfolios = result.scalars().all()

        if not portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        if portfolio_id not in [x.id for x in portfolios]:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        statement = delete(Portfolios).where(Portfolios.id == portfolio_id)
        await session.execute(statement)
        await session.commit()
        return {"status": "ok"}

    @staticmethod
    def to_pdf(items: list[dict]) -> io.BytesIO:
        buffer = io.BytesIO()

        pdfmetrics.registerFont(
            TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        )

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        styles["Title"].fontName = "DejaVu"
        styles["Normal"].fontName = "DejaVu"

        elements.append(Paragraph("Отчёт по портфелю", styles["Title"]))

        data = [
            ["Asset ID", "Название", "SECID", "Количество", "Средняя цена", "Текущая цена"]
        ]

        for item in items:
            data.append([
                item["id"],
                item["name"],
                item["secid"],
                item["quantity"],
                round(item["avg_price"], 2),
                round(item["current_price"], 2)
            ])

        table = Table(data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer