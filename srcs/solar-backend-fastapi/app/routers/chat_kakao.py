from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.logger import logger
from app.models.schemas import (
    ErrorResponse,
)
from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText
from app.services import ChatService, EmbeddingService
from app.services.function_call import FunctionCallService
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.post("/chat/kakao", response_model=KakaoBotChatResponse, responses={400: {"model": ErrorResponse}})
async def chat(
        kakao_request: KakaoBotChatRequest,
        chat_service: ChatService = Depends(ServiceFactory.get_chat_service),
        function_call_service: FunctionCallService = Depends(ServiceFactory.get_function_call_service),
        embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
) -> KakaoBotChatResponse:
    chat_request = kakao_request.to_chat_request(rag=True)

    ##################### Function Calling ######################

    messages = chat_request.messages
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_dining_recommendation",
                "description": "Get a list of dining recommendations asked by a user, \
                such as dining options nearby or in a specific region",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "region_name": {
                            "type": "string",
                            "description": "Choose region in Jeju Island categorized regarding direction.\
                            Region name e.g. east-kareum, al-kareum",
                        },
                        "message": {
                            "type": "string",
                            "description": "User inquiry about dining options",
                        },
                    },
                    "required": ["region_name", " mesage"],
                },
            },
        }
    ]

    response_message = await function_call_service.function_call(
        model=chat_request.model.value,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    tool_calls = response_message.tool_calls
    print(f'tool_calls: {tool_calls}')


    # if tool_calls:
    #     messages.append(response_message)
    #
    #     for tool_call in tool_calls:
    #         function_name = tool_call.function.name
    #         function_to_call = available_functions[function_name]
    #         function_args = json.loads(tool_call.function.arguments)
    #         print(f"function_args: {function_args}")
    #         function_response = function_to_call(
    #             message=chat_request.messages,
    #             location_name="제주하늘바람"
    #         )
    #
    #         # messages.append(
    #         #     {
    #         #         "tool_call_id": tool_call.id,
    #         #         "role": "tool",
    #         #         "name": function_name,
    #         #         "content": function_response, ## contexts
    #         #     }
    #         # )
    #
    # print(f'messages: {messages}')
    #
    # response = await chat_service.chat(messages=chat_request.messages,
    #                                    model=chat_request.model.value,
    #                                    contexts=contexts)

    # return self.open_ai_client.chat.completions.create(model=model, messages=messages)['message'].content

    ##################### Function Calling ######################

    try:
        response = None
        if chat_request.rag:
            embedding_collection = chat_request.collection if chat_request.collection else None
            contexts = await embedding_service.rag(messages=chat_request.messages,
                                                   embedding_collection=embedding_collection)
            logger.info(f'contexts: {contexts}')
            response = await chat_service.chat(messages=chat_request.messages,
                                               model=chat_request.model.value,
                                               contexts=contexts)
        return KakaoBotChatResponse(
            version="2.0",
            template=Template(
                outputs=[
                    Output(
                        simpleText=SimpleText(
                            text=response
                        )
                    )
                ]
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
