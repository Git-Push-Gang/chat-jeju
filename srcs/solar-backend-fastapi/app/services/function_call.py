from typing import List

from fastapi import HTTPException
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage


class FunctionCallService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    async def function_call(self,
                            messages: List[str],
                            tools,  # TODO 타입 입력
                            tool_choice,  # TODO 타입 입력
                            model: str = 'solar-1-mini-chat') -> ChatCompletionMessage:

        try:
            return self.open_ai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            ).choices[0].message
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
