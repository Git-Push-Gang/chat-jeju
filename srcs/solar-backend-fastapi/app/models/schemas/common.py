import json
from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    message: str = Field("OK", description="Message")
    statusCode: str = Field("200", description="Status code")
    data: Any


class ErrorResponse(BaseModel):
    message: str = Field(..., description="Error message")
    statusCode: str = Field(..., description="Status code")


SYSTEM_PROMPT = json.dumps({
    "role": "system",
    "content": "You're good at summarizing. Limit your answer to a maximum of three items. " +
               "Limit the length of your answer to 300 characters."
})
