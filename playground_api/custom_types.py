from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from playground_api.database import get_session
from playground_api.schemas import PaginationParams

T_Database = Annotated[AsyncSession, Depends(get_session)]
T_Pagination = Annotated[PaginationParams, Query()]
