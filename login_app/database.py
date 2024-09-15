import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import dotenv_values

env_vars = dotenv_values()
HOST = env_vars.get("HOST")
USER = env_vars.get("USER")
PASSWORD = env_vars.get("PASSWORD")
PORT = env_vars.get("PORT")
DATABASE = env_vars.get("DATABASE")

DATABASE_URL = f"mysql+asyncmy://{env_vars['USER']}:{env_vars['PASSWORD']}@{env_vars['HOST']}:{env_vars['PORT']}/{env_vars['DATABASE']}"

# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an asynchronous session maker
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db


async def read_query(sql: str, sql_params=()):
    async with SessionLocal() as db:
        try:
            result = await db.execute(text(sql), sql_params)
            return result.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

async def update_query(sql: str, sql_params=()):
    async with SessionLocal() as db:
        async with db.begin():
            try:
                await db.execute(text(sql), sql_params)
                await db.commit()
                return "success"
            except Exception as e:
                await db.rollback()
                print(f"An error occurred during update: {e}")
                return "failure"