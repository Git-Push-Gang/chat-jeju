from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText
from app.models.schemas import(
    ChatRequest,
    ChatResponse,
    ErrorResponse,
)
from app.services.chat import ChatService
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.post("/chat/kakao", response_model=KakaoBotChatResponse, responses={400: {"model": ErrorResponse}})
async def chat(
    kakao_request: KakaoBotChatRequest, 
    chat_service: ChatService = Depends(ServiceFactory.get_chat_service)
    ) -> ChatResponse | StreamingResponse:
    request = kakao_request.to_chat_request()
    if request.stream:
        response = await chat_service.stream_chat(messages=request.messages, model=request.model)

        return StreamingResponse(
            content=response,
            media_type="text/event-stream")
    else:
        response = await chat_service.chat(messages=request.messages, model=request.model)

        return KakaoBotChatResponse(
            version="2.0",
            template=Template(
                outputs=[
                    Output(
                        simpleText=SimpleText(
                            text=response.message
                        )
                    )
                ]
            )
        )
