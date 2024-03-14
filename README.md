# Сервис регистрации на сайте через telegram

## Реализация сервиса с использованием следующих технологиий:
![Python](https://img.shields.io/badge/Python-333?style=for-the-badge&logo=python&logoColor=yellow)
![Aiogram](https://img.shields.io/badge/aiogram-333?style=for-the-badge&logo=aiogram&logoColor=#009688)
![jwt](https://img.shields.io/badge/jwt-333?style=for-the-badge&logo=jwt&logoColor=#009688)
![bcrypt](https://img.shields.io/badge/bcrypt-333?style=for-the-badge&logo=bcrypt&logoColor=#009688)
![FastAPI](https://img.shields.io/badge/FastAPI-333?style=for-the-badge&logo=FastAPI&logoColor=#009688)
![Asyncio](https://img.shields.io/badge/Asyncio-333?style=for-the-badge&logo=Asyncio)
![Uvicorn](https://img.shields.io/badge/Uvicorn-333?style=for-the-badge&logo=Uvicorn)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-333?style=for-the-badge&logo=PostgreSQL)

## /start

Бот генерирует для пользователя уникальную ссылку для регистрации (токен для регистрации), действующую 1 минуту

## Ссылка для регистрации

Пользователь переходит по полученной ссылке, происходит обработка GET запроса: время жизни ссылки 60 секунд не истекло, а также проверка подписи токена с использованием секретного ключа, с которым создавался токен. 

## Страница ввода пароля для регистрации

Открывается веб-интерфейс с полем для ввода пароля и кнопкой "Зарегистрироваться". Нажатие кнопки приводит к отправке POST запроса на URL адрес, указанный в переменной окружения URL_ADDRES_TO_REGISTER.

## Обработка POST запроса

Сервер получает данные от пользователя после ввода пароля и нажатия кнопки "Зарегистрироваться". Происходит валидация токена. Валидация на пустое поле "password". А также проверка на наличие пользователя в базе данных.

## Регистрация на сайте

Регистрация происходит по данным пользователя из telegram, а именно: ID пользователя.

Если валидация токена прошла успешно, а также пользователя с таким ID пользователя ещё не существует в базе данных, то происходит успешная запись нового пользователя (страница register_done.html), иначе - сообщение об ошибке регистрации (страница register_error.html).

## Для запуска приложения

Клонировать репозиторий.

Создать виртуальное окружение.

Установить все зависимости из файла requirements.txt

Установить СУБД PostgreSQL. Создать там новую БД DB_NAME=telegram_test и нового пользователя DB_USER=telegram_user_test.

Создать файл .ENV и записать в него следующие переменные:

HTTP_API_TELEGRAM_TOKEN - токен, полученный при регистрации нового телеграм-бота от главного бота BotFather

JWT_SECRET_KEY - строка текста, на основании которого будет генерироваться токен по алгоритму HS256

URL_ADDRES_TO_REGISTER - url адрес, на который требуется отправить POST запрос с данными пользователя для регистрации

Запустить файл insert_data_db.py для наполнения таблцы БД тестовыми данными.

Запустить файл bot_run.bat

Зайти в телеграм бот по ссылке:
[Register_user_test_bot](https://t.me/Register_user_test_bot)

Нажать на кнопку /start для получения ссылки для регистрации

## License
Project Weather is licensed under the MIT license. (http://opensource.org/licenses/MIT)
