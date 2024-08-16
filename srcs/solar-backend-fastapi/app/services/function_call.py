import traceback

from fastapi import HTTPException
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from app.core.logger import logger
from app.services.measure_time import measure_time


class FunctionCallService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    @measure_time
    async def select_tool_calls(self,
                                messages,
                                tools,  # TODO 타입 입력
                                tool_choice,  # TODO 타입 입력
                                model: str = 'solar-1-mini-chat') -> ChatCompletionMessage:

        print(f'messages: {messages}')
        print(f'tools: {tools}')
        try:
            return self.open_ai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            ).choices[0].message
        except Exception as e:
            logger.error(f"## Error occurred. error: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
