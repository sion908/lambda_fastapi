from typing import AsyncIterator

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreate


async def get_user_query(
    db: AsyncSession,
    user_id: str
) -> AsyncIterator[User]:
    return db.scalar(
        select(User).where(User.id == user_id)
    )


async def create_user_query(db: AsyncSession, user: UserCreate) -> User:
    """create user by email and password"""
    db_user = User(**user.model_dump())

    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error:{e}")

    await db.refresh(db_user)
    return db_user
