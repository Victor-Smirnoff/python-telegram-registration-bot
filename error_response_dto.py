from pydantic import BaseModel


class ErrorResponseDTO(BaseModel):
    status_code: str
    detail: str
