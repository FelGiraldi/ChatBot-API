from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

# Motor asíncrono
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Factory de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para los modelos
class Base(DeclarativeBase):
    pass

# Dependencia para inyectar la DB en los endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session