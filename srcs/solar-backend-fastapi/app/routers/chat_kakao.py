from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.logger import logger
from app.models.schemas import (
    ErrorResponse,
)
from app.models.schemas.KakaoBotChatRequest import KakaoBotChatRequest
from app.models.schemas.KakaoBotChatResponse import KakaoBotChatResponse, Template, Output, SimpleText
from app.services import ChatService, EmbeddingService
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.post("/chat/kakao", response_model=KakaoBotChatResponse, responses={400: {"model": ErrorResponse}})
async def chat(
        kakao_request: KakaoBotChatRequest,
        chat_service: ChatService = Depends(ServiceFactory.get_chat_service),
        embedding_service: EmbeddingService = Depends(ServiceFactory.get_embedding_service),
) -> KakaoBotChatResponse:
    chat_request = kakao_request.to_chat_request(rag=True)

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
        raise HTTPException(status_code=400, detail=str(e))
