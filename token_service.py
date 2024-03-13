import datetime
import jwt


async def generate_jwt_registration_token(
    user_id: int,
    jwt_secret_key: str
) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=1)
    }

    token = jwt.encode(
        payload=payload,
        key=jwt_secret_key,
        algorithm="HS256",
    )

    return token
