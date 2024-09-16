from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import SQLAlchemyError

from login_app.database.database import Base, get_db


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default='user')

    @classmethod
    async def get_user(cls, column: str, value: str | int):
        valid_columns = {'email': cls.email, 'user_id': cls.user_id}

        async for session in get_db():
            try:
                query = select(cls).filter(valid_columns[column] == value)
                result = await session.execute(query)
                user = result.scalars().first()
                return user
            except SQLAlchemyError as e:
                print(f"An error occurred during get_user: {e}")
                return None

    @classmethod
    async def register(cls, email: str, hashed_password: bytes) -> dict:
        new_user = cls(email=email, password=hashed_password)

        async for session in get_db():
            try:
                session.add(new_user)
                await session.commit()
                return {"message": "User registered successfully!"}
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"An error occurred during register: {e}")
                return {"error": "Failed to register user"}
