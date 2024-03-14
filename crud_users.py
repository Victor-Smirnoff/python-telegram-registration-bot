from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from model import User


class CRUDUser:
    """
    Класс для выполнения основных операций в БД telegram_test над таблицей Users
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_by_telegram_user_id(self, telegram_user_id: int) -> User | None:
        """
        Метод возвращает найденный объект класса User если он найден в БД, иначе объект None
        :param telegram_user_id: айди пользователя
        :return: объект класса User или None
        """
        try:
            stmt = select(User).where(User.user_id == telegram_user_id)
            result: Result = await self.session.execute(stmt)
            if isinstance(result, Result):
                user = result.scalar()
                if isinstance(user, User):
                    return user
                else:
                    return None
        except SQLAlchemyError:
            return None

    async def create_user(
            self,
            user_id: int,
            password: str,
    ) -> User | None:
        """
        Метод записывает нового пользователя в БД
        :param user_id: телеграм айди пользователя
        :param password: строка - хэшированное значение пароля
        :return: объект класса User | None
        """

        if not all((user_id, password)):
            return None

        try:
            new_user = User(user_id=user_id, password=password)
            self.session.add(new_user)
            try:
                await self.session.commit()
                await self.session.refresh(new_user)
                return new_user
            except IntegrityError:
                return None
        except SQLAlchemyError:
            return None
