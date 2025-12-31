import asyncio
from app.core.database import engine, Base
from app.models.sql_models import Conversation, Message # Importar para que sean detectados

async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    asyncio.run(init_tables())