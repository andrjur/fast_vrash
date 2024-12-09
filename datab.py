from database import engine, new_session
from models import Model, UserOrm
from users import get_password_hash

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

async def create_user(username: str, password: str):
    async with new_session() as session:
        user = UserOrm(username=username, hashed_password=get_password_hash(password))
        session.add(user)
        await session.commit()