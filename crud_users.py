from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from database import db_helper
from error_response_dto import ErrorResponseDTO
from model import User


class CRUDUser:
    """
    Класс для выполнения основных операций в БД telegram_test над таблицей Users
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_user_by_telegram_user_id(self, telegram_user_id: int) -> User | ErrorResponseDTO:
        """
        Метод возвращает найденный объект класса User если он найден в БД, иначе объект ErrorResponseDTO
        :param telegram_user_id: айди пользователя
        :return: объект класса User или ErrorResponseDTO
        """
        try:
            stmt = select(User).where(User.user_id == telegram_user_id)
            result: Result = await self.session.execute(stmt)
            if isinstance(result, Result):
                user = result.scalar()
                if isinstance(user, User):
                    return user
                else:
                    response = ErrorResponseDTO(
                        status_code=404,
                        detail=f"Пользователь с айди {telegram_user_id} не найден"
                    )
                    return response

        except SQLAlchemyError as e:
            response = ErrorResponseDTO(
                status_code=500,
                detail=f"База данных недоступна",
                error_name=str(e)
            )
            return response

    async def create_user(
        self,
        user_id: int,
        password: str,
    ) -> User | ErrorResponseDTO:
        """
        Метод записывает нового пользователя в БД
        :param user_id: телеграм айди пользователя
        :param password: строка - хэшированное значение пароля
        :return: объект класса User | ErrorResponseDTO
        """
        try:
            new_user = User(user_id=user_id, password=password)
            self.session.add(new_user)
            try:
                await self.session.commit()
                await self.session.refresh(new_user)
                return new_user
            except IntegrityError as e:
                response = ErrorResponseDTO(
                    status_code=409,
                    detail=f"Пользователь с айди “{user_id}” уже был зарегистрирован",
                    error_name=str(e)
                )
                return response

        except SQLAlchemyError as e:
            response = ErrorResponseDTO(
                status_code=500,
                detail=f"База данных недоступна",
                error_name=str(e)
            )
            return response


async def crud_user(session: AsyncSession = Depends(db_helper.session_dependency)):
    return CRUDUser(session=session)
