from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from model.line_contents import LineContents
from schema.line import LineContentsCreate


async def insert_data(session: AsyncSession, content: LineContentsCreate) -> bool:
    stmt = insert(LineContents).values(**content.model_dump())
    await session.execute(stmt)
    await session.commit()
    return True


async def fetch_data_one(session: AsyncSession, content_type: str):
    stmt = select(LineContents).where(LineContents.content_type == content_type)
    result = await session.execute(stmt)
    return result.scalar()


async def delete_data_one(session: AsyncSession, content_id: str):
    stmt = select(LineContents).where(LineContents.content_id == content_id)
    result = await session.execute(stmt)
    if target := result.scalar():
        await session.delete(target)
        await session.commit()
    return True
