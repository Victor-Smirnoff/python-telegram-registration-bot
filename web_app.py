import uvicorn
import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from crud_users import CRUDUser, crud_user
from error_response_dto import ErrorResponseDTO
from model import User
from password_service import generate_hashed_password
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
    except ExpiredSignatureError as e:
        error_response = ErrorResponseDTO(
            status_code=403,
            detail=f"Срок действия токена “{jwt_token}” истек",
            error_name=str(e)
        )

        error_message = error_response.detail
        status_code = error_response.status_code

        return templates.TemplateResponse(
            name="register_error.html",
            context={"request": request, "error_message": error_message},
            status_code=status_code
        )


@app.post("/users/register/", response_class=HTMLResponse)
async def post_register_page(
    request: Request,
    registration_token: str = Form(...),
    password: str = Form(""),
    crud_user_obj: CRUDUser = Depends(crud_user)
):
    if type(password) is str and password == "":
        error_response = ErrorResponseDTO(
            status_code=400,
            detail=f"Был введен пустой пароль"
        )
        error_message = error_response.detail
        status_code = error_response.status_code
        return templates.TemplateResponse(
            name="register_error.html",
            context={"request": request, "error_message": error_message},
            status_code=status_code
        )

    try:
        payload = await decode_jwt_token(
            jwt_token=registration_token,
            jwt_secret_key=JWT_SECRET_KEY
        )

        user_id = int(payload["sub"])

        hashed_password = await generate_hashed_password(password=password)
        hashed_password_str = hashed_password.decode()
        new_user = await crud_user_obj.create_user(user_id=user_id, password=hashed_password_str)

        if isinstance(new_user, User):
            token = {"registration_token": registration_token}
            return templates.TemplateResponse(
                name="register_done.html",
                context={"request": request, "token": token, "new_user": new_user},
                status_code=201
            )
        elif isinstance(new_user, ErrorResponseDTO):
            error_response = new_user
            error_message = error_response.detail
            status_code = error_response.status_code
            return templates.TemplateResponse(
                name="register_error.html",
                context={"request": request, "error_message": error_message},
                status_code=status_code
            )

    except ExpiredSignatureError as e:
        error_response = ErrorResponseDTO(
            status_code=403,
            detail=f"Срок действия токена “{registration_token}” истек",
            error_name=str(e)
        )

        error_message = error_response.detail
        status_code = error_response.status_code

        return templates.TemplateResponse(
            name="register_error.html",
            context={"request": request, "error_message": error_message},
            status_code=status_code
        )


if __name__ == "__main__":
    uvicorn.run("web_app:app", reload=True)
