from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException

from app.core.logger import logger
from app.models.schemas import (
    ErrorResponse, )
from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText
from app.services import ChatService, EmbeddingService
from app.services.function_call import FunctionCallService
from app.services.langid import LangIdService
from app.services.measure_time import measure_time
from app.services.service_factory import ServiceFactory
from app.services.tools.init_functions import function_descriptions, functions
from app.services.translation import TranslationService

router = APIRouter()


@measure_time
@router.post("/chat/kakao", response_model=KakaoBotChatResponse, responses={400: {"model": ErrorResponse}})
async def chat(
        kakao_request: KakaoBotChatRequest,
        langid_service: LangIdService = Depends(ServiceFactory.get_langid_service),
        translation_service: TranslationService = Depends(ServiceFactory.get_translation_service),
        chat_service: ChatService = Depends(ServiceFactory.get_chat_service),
        function_call_service: FunctionCallService = Depends(ServiceFactory.get_function_call_service),
        embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
) -> KakaoBotChatResponse:
    try:
        logger.info(f'-- kakao_request: {kakao_request}')

        lang = await langid_service.get_language_id(messages=[kakao_request.userRequest.utterance])
        logger.info(f'lang: {lang}')
        # ["en", "ko"] 형태로 반환됨
        # if lang[0] == "en":
        #     kakao_request.userRequest.utterance = await translation_service.get_en_ko_translation(kakao_request.userRequest.utterance)

        request = kakao_request.to_chat_request()
        user_utterances = request.messages
        messages_with_role = [{
            "role": "user",
            "content": user_utterances[0]
        }]

        # Tool Calls Selection
        tool_calls = await function_call_service.select_tool_calls(
            region_name=kakao_request.action.params['region_name'],
            category_name=kakao_request.action.params['category_name'],
            messages=messages_with_role,
            tools=function_descriptions,
            tool_choice="auto",
        )

        print(f'tool_calls: {tool_calls}')

        if tool_calls:

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                logger.info(f'function_args: {function_args}')

                # Function Calling with RAG
                if function_name == "get_detailed_information_of_a_specific_stay":
                    arg = function_args.get("stay_name")
                    contexts = function_to_call(stay_name=arg)
                else:
                    contexts = await function_to_call(
                        messages=request.messages,
                        region_name=(kakao_request.action.params['region_name']),
                        embedding_service=embedding_service
                    )
                print(f'---- contexts: {contexts}')

                final_response = await chat_service.chat(messages=user_utterances,
                                                         model=request.model.value,
                                                         contexts=contexts)

                if lang[0] == "en":
                    final_response = await translation_service.get_ko_en_translation(final_response)

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
