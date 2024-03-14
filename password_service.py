import bcrypt


async def generate_hashed_password(password: str) -> bytes:
    """
    Функция принимает пароль от пользователя и делает из него хэшированную строку байтов
    :param password: строка пароля
    :return: хэшированная строка байтов
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


async def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Функция сравнивает строку пароля от пользователя и строку этого же пароля из базы данных
    :param plain_password: обычный пароль, который ввел пользователь
    :param hashed_password: строковое представление пароля пользователя из базы данных
    :return: bool - True если пароли совпадают, иначе - False
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
