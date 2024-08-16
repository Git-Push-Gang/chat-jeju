import aiohttp
import json
from typing import List

class LangIDCallService:

    async def get_language_id(self, messages: List[str]) -> List[str]:
        """
        Args:
            messages (List[str]): List of texts to identify the language of.

        Returns:
            List[str]: List of language responses e.g. ["en", "ko"]
        """
        # Define the URL of the language identification service
        url = "http://langid:9008/detect"
        
        # Create a session object
        async with aiohttp.ClientSession() as session:
            # List to store language detection results
            results = []
            
            # Process each message in the list
            for message in messages:
                # Prepare the data payload
                payload = {'q': message}
                
                # Send POST request and await the response
                async with session.post(url, data=payload) as response:
                    # Read the response as JSON
                    response_data = await response.json()
                    
                    # Extract the language from the response
                    language = response_data.get('responseData', {}).get('language', 'unknown')
                    results.append(language)
                    
            return results

# Usage example
# lang_service = LangIDCallService()
# languages = await lang_service.get_language_id(["This is a test", "Este es un test"])
# print(languages)