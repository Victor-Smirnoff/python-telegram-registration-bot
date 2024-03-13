import datetime
import jwt


async def generate_jwt_registration_token(
    user_id: int,
    jwt_secret_key: str
) -> str:
    """
    Функция создает jwt_registration_token для пользователя по его user_id
    :param user_id: айди пользователя telegram
    :param jwt_secret_key: секретный ключик из файла .ENV
    :return: jwt токен для регистрации пользователя со сроком жизни 60 секунд
    """
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=60)
    }

    token = jwt.encode(
        payload=payload,
        key=jwt_secret_key,
        algorithm="HS256",
    )

    return token


async def decode_jwt_token(
        jwt_token: str,
        jwt_secret_key: str
):
    """
    Функция декодирует данные из jwt токена и возвращает словарь payload с данными user_id и времени жизни токена
    :param jwt_token: jwt токен для регистрации
    :param jwt_secret_key: секретный ключик из файла .ENV
    :return: словарь payload с данными user_id - айди пользователя telegram
    и exp - целое число в формате UNIX, до которого можно считать токен рабочим
    """
    payload = jwt.decode(
        jwt=jwt_token,
        key=jwt_secret_key,
        algorithms=["HS256"],
        verify=True
    )

    return payload
