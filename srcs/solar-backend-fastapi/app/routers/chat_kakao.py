from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.logger import logger
from app.models.schemas import (
    ErrorResponse, )
from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText
from app.services import ChatService, EmbeddingService
from app.services.function_call import FunctionCallService
from app.services.measure_time import measure_time
from app.services.service_factory import ServiceFactory
from app.services.tools.init_functions import function_descriptions, functions

router = APIRouter()


@measure_time
@router.post("/chat/kakao", response_model=KakaoBotChatResponse, responses={400: {"model": ErrorResponse}})
async def chat(
        kakao_request: KakaoBotChatRequest,
        chat_service: ChatService = Depends(ServiceFactory.get_chat_service),
        function_call_service: FunctionCallService = Depends(ServiceFactory.get_function_call_service),
        embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
) -> KakaoBotChatResponse:
    logger.info(f'-- kakao_request: {kakao_request}')
    request = kakao_request.to_chat_request()
    try:
        user_utterances = request.messages
        messages_with_role = [{
            "role": "user",
            "content": user_utterances[0]
        }]

        # Tool Calls Selection
        tool_calls_response = await function_call_service.select_tool_calls(
            messages=messages_with_role,
            tools=function_descriptions,
            tool_choice="auto",
        )
        tool_calls = tool_calls_response.tool_calls
        print(f'tool_calls: {tool_calls}')

        if tool_calls:

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = functions[function_name]

                # Function Calling with RAG
                contexts = await function_to_call(
                    messages=user_utterances,  # rag 를 위한 function 에서는 사용자 발화만 전달함
                    region_name="east-kareum",  # 1차적으로 고정값 사용
                    embedding_service=embedding_service
                )
                print(f'---- contexts: {contexts}')

                final_response = await chat_service.chat(messages=user_utterances,
                                                         model=request.model.value,
                                                         contexts=contexts)
                return KakaoBotChatResponse(
                    version="2.0",
                    template=Template(
                        outputs=[
                            Output(
                                simpleText=SimpleText(
                                    text=final_response
                                )
                            )
                        ]
                    )
                )
        else:
            # TODO function calling 이 찾지 못한 경우 전체 컬렉션 조회?
            raise HTTPException(status_code=500, detail=str("적절한 함수를 찾을 수 없음."))


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
