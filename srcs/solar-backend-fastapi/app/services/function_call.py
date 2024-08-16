from __future__ import annotations

import traceback
from typing import Iterable

from fastapi import HTTPException
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionToolParam, \
    ChatCompletionToolChoiceOptionParam

from app.core.logger import logger
from app.services.measure_time import measure_time


class FunctionCallService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    @measure_time
    async def select_tool_calls(self,
                                messages,
                                tools: Iterable[ChatCompletionToolParam],
                                tool_choice: ChatCompletionToolChoiceOptionParam,
                                model: str = 'solar-1-mini-chat') -> ChatCompletionMessage:
        try:
            return self.open_ai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            ).choices[0].message
        except Exception as e:
            logger.error(f"## Error occurred. error: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
