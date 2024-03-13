import uvicorn
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from token_service import decode_jwt_token
from jwt.exceptions import ExpiredSignatureError


load_dotenv()

app = FastAPI()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

templates = Jinja2Templates(directory="templates")


@app.get("/users/register/{jwt_token}", response_class=HTMLResponse)
async def get_register_page(jwt_token: str, request: Request):
    try:
        payload = await decode_jwt_token(
            jwt_token=jwt_token,
            jwt_secret_key=JWT_SECRET_KEY
        )
        return templates.TemplateResponse(
            name="register.html",
            context={"request": request, "payload": payload, "jwt_token": jwt_token},
            status_code=200
        )
    except ExpiredSignatureError:
        error_message = f"Срок действия токена “{jwt_token}” истек"
        return templates.TemplateResponse(
            name="register_error.html",
            context={"request": request, "error_message": error_message},
            status_code=403
        )


@app.post("/users/register/", response_class=HTMLResponse)
async def post_register_page(request: Request, registration_token: str = Form(...), password: str = Form(...)):
    #  здесь должен быть блок кода, который проверяет айди пользователя в базе данных
    #  если пользователь не найден, то происходит запись в таблицу users
    #  если пользователь с таким айди уже существует, то перенаправление на страницу с ошибкой регистрации

    #  здесь будет описан сценарий если с базой данных всё ок и запись прошла успешно и если пароль отправлен не пустой

    token = {"registration_token": registration_token}

    return templates.TemplateResponse(
        name="register_done.html",
        context={"request": request, "token": token},
        status_code=201
    )


if __name__ == "__main__":
    uvicorn.run("web_app:app", reload=True)
