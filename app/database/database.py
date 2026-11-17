from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

engine = create_async_engine(url=settings.DB_URL, echo=False)
engine_null_pool = create_async_engine(
    url=settings.DB_URL, poolclass=NullPool, echo=False
)
test_engine = create_async_engine(
    settings.TEST_DATABASE_URL, poolclass=NullPool, echo=False
)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pool, expire_on_commit=False
)
async_test_session_maker = async_sessionmaker(bind=test_engine, expire_on_commit=False)
