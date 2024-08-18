from typing import List, Dict, AsyncGenerator, Optional

from app.clients import OpenAIClient
from app.models.schemas import EmbeddingContextList, SYSTEM_PROMPT
from app.services.measure_time import measure_time


class ChatService:

    def __init__(self, open_ai_client: OpenAIClient):
        self.open_ai_client = open_ai_client

    def get_message(self, messages: str, contexts: Optional[EmbeddingContextList], ) -> List[Dict[str, str]]:
        """
        Generate message for chat

        Args:
            contexts:
            messages (str): List of messages

        Returns:
            List[Dict[str, str]]: List of messages
        """
        nl = '\n'
        if contexts and hasattr(contexts, 'context') and contexts.context:
            contexts = [f"'Context: {f'{nl}'.join([context.text for context in contexts.context])}'"]
        else:
            contexts = [contexts]
        user_utterance = f"User Inquiry: {messages}"

        combined_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "\n".join(contexts + [user_utterance])
            },
        ]
        return combined_messages

    @measure_time
    async def chat(self,
                   messages: List[str],
                   contexts: Optional[EmbeddingContextList],
                   model: str = 'solar-1-mini-chat') -> str:
        """
        Request completion from OpenAI API
        If you want to add extra logic, you can add it here. e.g. filtering, validation, rag, etc.

        Args:
            contexts:
            messages (List[str]): List of messages
            model (str, optional): Model name. Defaults to 'solar-1-mini-chat'.

        Returns:
            str: Completion response
        """
        response = await self.open_ai_client.generate(messages=self.get_message(messages, contexts), model=model)

        return response

    @measure_time
    async def stream_chat(self, messages: List[str], contexts: Optional[EmbeddingContextList],
                          model: str = 'solar-1-mini-chat') -> AsyncGenerator:
        """
        Request stream completion from OpenAI API
        If you want to add extra logic, you can add it here. e.g. filtering, validation, rag, etc.

        Args:
            contexts:
            messages (List[str]): List of messages
            model (str, optional): Model name. Defaults to 'solar-1-mini

        Returns:
            AsyncGenerator: Stream completion response
        """

        response = self.open_ai_client.stream_generate(messages=self.get_message(messages, contexts), model=model)

        return response
