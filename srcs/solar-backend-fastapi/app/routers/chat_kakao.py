from __future__ import annotations

import asyncio
import json

import httpx
from fastapi import APIRouter, HTTPException, Depends

from app.core.logger import logger
from app.models.schemas import ErrorResponse
from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText, Data
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
async def chat(kakao_request: KakaoBotChatRequest,
               langid_service: LangIdService = Depends(ServiceFactory.get_langid_service),
               translation_service: TranslationService = Depends(
                   ServiceFactory.get_translation_service),
               chat_service: ChatService = Depends(ServiceFactory.get_chat_service),
               function_call_service: FunctionCallService = Depends(
                   ServiceFactory.get_function_call_service),
               embedding_service: EmbeddingService = Depends(
                   ServiceFactory.get_embedding_service),
               ) -> KakaoBotChatResponse:
    try:
        logger.info(f'-- kakao_request: {kakao_request}')
        langs = await langid_service.get_language_id(messages=[kakao_request.userRequest.utterance])

        asyncio.create_task(process_and_send_callback(kakao_request,
                                                      langs,
                                                      translation_service,
                                                      chat_service,
                                                      function_call_service,
                                                      embedding_service,
                                                      ))
        logger.info("process_and_send_callback requested.")
        return create_initial_response(langs[0])
    except Exception as e:
        logger.error(f"##### error: f{e}")
        raise HTTPException(status_code=500, detail=str(e))


def create_initial_response(lang: str):
    if lang == 'ko':
        text = "잠시만 기다려 주시면 곧 답변 드리겠습니다."
    else:
        text = "Please hold on for a moment. I’ll respond shortly."
    return KakaoBotChatResponse(
        useCallback=True,
        data=Data(text=text))


async def process_and_send_callback(request: KakaoBotChatRequest,
                                    langs: [str],
                                    translation_service: TranslationService,
                                    chat_service: ChatService,
                                    function_call_service: FunctionCallService,
                                    embedding_service: EmbeddingService):
    user_utterances = [request.userRequest.utterance]
    messages_with_role = [{
        "role": "user",
        "content": user_utterances[0]
    }]

    # Tool Calls Selection
    tool_calls = await function_call_service.select_tool_calls(
        region_name=request.action.params.get('region_name', None),
        category_name=request.action.params.get('category_name', None),
        messages=messages_with_role,
        tools=function_descriptions,
        tool_choice="auto",
    )
    logger.info(f'tool_calls: {tool_calls}')

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
                logger.info(f"--before function call")
                contexts = await function_to_call(
                    messages=user_utterances,
                    region_name=function_args.get("region_name"),
                    embedding_service=embedding_service
                )
            logger.info("## function call with contexts executed.")

            final_response = await chat_service.chat(messages=user_utterances,
                                                     model="solar-1-mini-chat",
                                                     contexts=contexts)
            logger.info("## The final response is ready.")

            if "en" in langs:
                logger.info(f"## [TRANSLATION] requested.")
                final_response = await translation_service.get_ko_en_translation(final_response)
                logger.info(
                    f"## [TRANSLATION] The translated final response is ready. final_response: {final_response}")

            async with httpx.AsyncClient() as client:
                logger.info(f"Callback URL: {request.userRequest.callbackUrl}")
                final_response_from_kakao = await client.post(url=request.userRequest.callbackUrl,
                                                              json=json.dumps(create_final_kakao_response(final_response)))
                logger.info(f"## [FINAL_RESPONSE_FROM_KAKAO] {final_response_from_kakao}")
    else:
        raise HTTPException(status_code=500, detail=str("Could not find an appropriate tool_calls."))


def create_final_kakao_response(final_text):
    return KakaoBotChatResponse(
        template=Template(
            outputs=[Output(
                simpleText=SimpleText(text=final_text))]))
