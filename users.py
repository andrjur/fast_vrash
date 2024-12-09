from passlib.context import CryptContext
from sqlalchemy import select
from datab import new_session
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



async def get_user(username: str):
    async with new_session() as session:
        query = select(UserOrm).where(UserOrm.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user 