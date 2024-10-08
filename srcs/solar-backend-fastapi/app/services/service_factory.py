import os
from typing import Dict

from openai import OpenAI

from app.clients import OpenAIClient, UpstageClient
from app.services import ChatService, EmbeddingService
from app.services.function_call import FunctionCallService
from app.services.langid import LangIdService
from app.services.translation import TranslationService


class ServiceFactory:
    base_urls: Dict[str, OpenAIClient] = {
        'solar': "https://api.upstage.ai/v1/solar"
    }

    @classmethod
    def get_chat_service(cls, client_name: str = 'solar') -> ChatService:
        return ChatService(
            open_ai_client=OpenAIClient(base_url=cls.base_urls[client_name]))

    @classmethod
    def get_function_call_service(cls, client_name: str = 'solar') -> FunctionCallService:
        return FunctionCallService(
            open_ai_client=OpenAI(api_key=os.getenv("API_KEY"), base_url=cls.base_urls[client_name]))

    @classmethod
    def get_embedding_service(cls, client_name: str = 'solar') -> EmbeddingService:
        return EmbeddingService(
            open_ai_client=OpenAIClient(base_url=cls.base_urls[client_name]),
            upstage_client=UpstageClient(base_url=cls.base_urls[client_name]))

    @classmethod
    def get_langid_service(cls) -> LangIdService:
        return LangIdService()

    @classmethod
    def get_translation_service(cls, client_name: str = 'solar') -> TranslationService:
        return TranslationService(open_ai_client=OpenAI(api_key=os.getenv("API_KEY"), base_url=cls.base_urls[client_name]))
