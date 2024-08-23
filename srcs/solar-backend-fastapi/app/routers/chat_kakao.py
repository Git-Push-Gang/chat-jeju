from __future__ import annotations

import asyncio
import json
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from httpx import RequestError, Client, TimeoutException

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
        text = "Please hold on for a moment.\nI’ll respond shortly."
    return KakaoBotChatResponse(
        useCallback=True,
        data=Data(text=text))


async def process_and_send_callback(
        request: KakaoBotChatRequest,
        langs: List[str],
        translation_service: TranslationService,
        chat_service: ChatService,
        function_call_service: FunctionCallService,
        embedding_service: EmbeddingService
):
    try:
        user_utterance = request.userRequest.utterance
        messages_with_role = [{"role": "user", "content": user_utterance}]

        tool_calls = await select_tool_calls(request, function_call_service, messages_with_role)

        if not tool_calls:
            raise ValueError("Could not find an appropriate tool_calls.")

        for tool_call in tool_calls:
            final_text = await process_tool_call(tool_call, user_utterance, embedding_service, chat_service)

            if "en" in langs:
                final_text = await translate_response(final_text, translation_service)

            callback_response = await send_callback_response(request.userRequest.callbackUrl, final_text)
            logger.info(f"Kakao response: {callback_response}")
    except Exception as e:
        logger.error(f"Error in process_and_send_callback: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


async def select_tool_calls(request, function_call_service, messages_with_role):
    tool_calls = await function_call_service.select_tool_calls(
        region_name=request.action.params.get('region_name'),
        category_name=request.action.params.get('category_name'),
        messages=messages_with_role,
        tools=function_descriptions,
        tool_choice="auto",
    )
    logger.info(f'Tool calls selected: {tool_calls}')
    return tool_calls


async def process_tool_call(tool_call, user_utterance, embedding_service, chat_service):
    function_name = tool_call.function.name
    function_to_call = functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    logger.info(f'Function arguments: {function_args}')

    if function_name == "get_detailed_information_of_a_specific_stay":
        contexts = function_to_call(stay_name=function_args.get("stay_name"))
    else:
        contexts = await function_to_call(
            messages=[user_utterance],
            region_name=function_args.get("region_name"),
            embedding_service=embedding_service
        )
    logger.info("Function call with contexts executed.")

    final_text = await chat_service.chat(
        messages=[user_utterance],
        model="solar-1-mini-chat",
        contexts=contexts
    )
    logger.info("Final response is ready.")
    return final_text


def create_kakao_response(final_text):
    return KakaoBotChatResponse(
        template=Template(
            outputs=[Output(simpleText=SimpleText(text=final_text))]
        )
    )


async def translate_response(final_text, translation_service):
    logger.info("Translation requested.")
    translated_text = await translation_service.get_ko_en_translation(final_text)
    logger.info(f"Translated final response: {translated_text}")
    return translated_text


async def send_callback_response(callback_url, final_text):
    final_response = create_kakao_response(final_text)
    with Client() as client:
        try:
            final_json = json.dumps(final_response, default=lambda o: o.__dict__, indent=2)
            logger.info(f"Final JSON: {final_json}")
            response = client.post(
                url=callback_url,
                json=final_json,
                timeout=1.0
            )
            logger.info(f"Kakao response: {response}")
        except TimeoutException:
            logger.error("Request timed out after 1 second")
        except RequestError as e:
            logger.error(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")