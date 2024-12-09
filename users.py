from passlib.context import CryptContext
from sqlalchemy import select
from database import new_session
from datab import UserOrm
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(username: str, password: str):
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