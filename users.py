from passlib.context import CryptContext
from sqlalchemy import select
from database import new_session
from models import UserOrm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(username: str):
    async with new_session() as session:
        query = select(UserOrm).where(UserOrm.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user