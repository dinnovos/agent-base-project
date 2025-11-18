import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Depends
from typing import Annotated

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# DB_URI = os.getenv("DB_URI")
DB_URI = "postgresql://postgres:zUBMRKsAxGvyImaTOkvJgvcEVduPWJjT@autorack.proxy.rlwy.net:50610/railway"

# Global checkpointer instance
_checkpointer: AsyncPostgresSaver | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _checkpointer
    async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
        _checkpointer = checkpointer
        await _checkpointer.setup()
        yield

def get_checkpointer() -> AsyncPostgresSaver:
    if _checkpointer is None:
        raise RuntimeError("Checkpointer not initialized. Make sure lifespan is running.")
    return _checkpointer

CheckpointerDep = Annotated[AsyncPostgresSaver, Depends(get_checkpointer)]