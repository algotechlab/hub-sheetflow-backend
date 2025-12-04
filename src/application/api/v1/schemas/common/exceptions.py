from typing import Optional

from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    code: str
    message: str


class MultipleExceptionItemSchema(ExceptionSchema):
    field: Optional[str] = None
