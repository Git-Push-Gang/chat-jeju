from app.clients import OpenAIClient

class TranslationService:

    def __init__(self, open_ai_client: OpenAIClient):
        self.open_ai_client = open_ai_client

    def get_en_ko_translation(self, message: str, model: str="solar-1-mini-translate-enko") -> str:
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

    def get_ko_en_translation(self, message: str, model: str="solar-1-mini-translate-koen") -> str:
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