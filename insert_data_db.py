import asyncio
from database import Base, db_helper
from model import User
from password_service import generate_hashed_password


engine = db_helper.engine
session_factory = db_helper.session_factory


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_users_for_test():
    users_list = [User(
        user_id=user_id,
        password=(await generate_hashed_password(str(user_id))).decode()
    ) for user_id in range(555555221, 555555251)]
    async with session_factory() as session:
        session.add_all(users_list)
        await session.commit()


async def main():
    await create_tables()
    await insert_users_for_test()


if __name__ == '__main__':
    asyncio.run(main())
