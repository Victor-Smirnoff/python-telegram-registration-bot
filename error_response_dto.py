from pydantic import BaseModel


class ErrorResponseDTO(BaseModel):
    status_code: int
    detail: str
    error_name: str | None = None
