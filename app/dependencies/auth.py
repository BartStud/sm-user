from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.dependencies.db import get_db
from app.models import ParentProfile


async def get_current_user(
    user=Depends(verify_token), db: AsyncSession = Depends(get_db)
):
    user_db = await db.execute(
        select(ParentProfile).where(ParentProfile.id == user["sub"])
    )
    user_db = user_db.scalar()
    if not user_db:
        user_db = ParentProfile(id=user["sub"])
        db.add(user_db)
        await db.commit()
        await db.refresh(user_db)
    return user, user_db


CurrentUserDep = Annotated[tuple[dict, ParentProfile], Depends(get_current_user)]
