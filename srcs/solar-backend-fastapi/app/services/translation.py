from openai import OpenAI

from app.services.measure_time import measure_time


class TranslationService:

    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    @measure_time
    async def get_en_ko_translation(self, message: str, model: str = "solar-1-mini-translate-enko") -> str:
        """
        Generate message for chat

        Args:
            message (str): List of messages

        Returns:
            message (str): Message for chat
        """

        stream = self.open_ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": message},
            ],
            stream=False,
        )

        translated_message = stream.choices[0].message.content

        return translated_message

    async def get_ko_en_translation(self, message: str, model: str = "solar-1-mini-translate-koen") -> str:
        """
        Generate message for chat

        Args:
            message (str): List of messages

        Returns:
            message (str): Message for chat
        """

        stream = self.open_ai_client.chat.completions.create(
            model=model,
            messages=[
                # {"role": "system", "content": "Translate the following Korean text into English. For proper nouns, write both the original and the translated name. For example, 'Seoul(서울)'."},
                {"role": "user", "content": message},
            ],
            stream=False,
        )

        translated_message = stream.choices[0].message.content

        return translated_message
