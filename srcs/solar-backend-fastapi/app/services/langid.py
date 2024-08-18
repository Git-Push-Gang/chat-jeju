from typing import List

import aiohttp

from app.core.logger import logger
from app.services.measure_time import measure_time


class LangIdService:

    @measure_time
    async def get_language_id(self, messages: List[str]) -> List[str]:
        """
        Args:
            messages (List[str]): List of texts to identify the language of.

        Returns:
            List[str]: List of language responses e.g. ["en", "ko"]
        """
        url = "http://langid:9008/detect"

        async with aiohttp.ClientSession() as session:
            results = []

            for message in messages:
                payload = message
                logger.info(f'payload: {payload}')

                async with session.post(url, data=payload) as response:
                    response_data = await response.json(content_type='text/javascript; charset=utf-8')
                    logger.info(f'response_data: {response_data}')

                language = response_data.get('responseData', {}).get('language', 'unknown')
                results.append(language)

            return results
