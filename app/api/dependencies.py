from typing import Annotated

from fastapi import Depends

from app.database.database import async_session_maker
from app.database.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
