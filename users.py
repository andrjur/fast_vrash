from passlib.context import CryptContext
from sqlalchemy import select
from datab import new_session
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(username: str, password: str):
    from datab import UserOrm
    async with new_session() as session:
        hashed_password = get_password_hash(password)
        user = UserOrm(username=username, hashed_password=hashed_password)
        session.add(user)
        await session.commit()

async def get_user(username: str):
    async with new_session() as session:
        query = select(UserOrm).where(UserOrm.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user 