from __future__ import annotations

import json
import traceback
from typing import Iterable

from fastapi import HTTPException
from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam, \
    ChatCompletionToolChoiceOptionParam, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function

from app.core.logger import logger
from app.services.measure_time import measure_time


class FunctionCallService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client
        self.category_name_to_function_name = {
            "attraction": "get_to_visit_recommendation",
            "dining": "get_dining_recommendation",
            "stay": "get_detailed_information_of_a_specific_stay",
            "entertainment": "get_to_do_recommendation",
        }

    @measure_time
    async def select_tool_calls(self,
                                region_name,
                                category_name,
                                messages,
                                tools: Iterable[ChatCompletionToolParam],
                                tool_choice: ChatCompletionToolChoiceOptionParam,
                                model: str = 'solar-1-mini-chat') -> list[ChatCompletionMessageToolCall] | None:
        if region_name and category_name:
            return [ChatCompletionMessageToolCall(
                id='',
                function=Function(
                    arguments=json.dumps({"message": (messages[0]['content']), "region_name": region_name},
                                         ensure_ascii=False),
                    name=self.category_name_to_function_name[category_name]),
                type='function')]
        else:
            try:
                return self.open_ai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                ).choices[0].message.tool_calls
            except Exception as e:
                logger.error(f"## Error occurred. error: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=str(e))
