import os
from google import genai
from google.genai.errors import APIError

class GeminiClient:
    """
    Wrapper for Google's Gemini API that supports both text and image inputs.
    """

    def __init__(self, api_key=None, model="gemini-2.5-flash-lite"):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("API key must be provided or set in the GEMINI_API_KEY environment variable.")

        self.client = genai.Client(api_key=key)
        self.model = model


    def _prepare_media_part(self, file_path):
        ext = file_path.lower().split(".")[-1]
        mime_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "ogg": "audio/ogg",
        }
        mime_type = mime_map.get(ext, None)
        if not mime_type:
            raise ValueError(f"Unsupported file type: {ext}")
        
        with open(file_path, "rb") as f:
            data = f.read()

        return {"inline_data": {"mime_type": mime_type, "data": data}}


    def get_response(self, query: str, images=None, audio=None) -> str:
        """
        Generates content from the Gemini model based on text and optional image inputs.
        Args:
            query  : Text prompt to send to the model.
            images : Optional list of image file paths or base64 dicts.
            audio  : Individual audio files or soundtracks from videos.
        Returns:
            Model's textual response.
        """

        try:
            # Always start with a text part
            parts = [{"text": query}]

            # Add image parts if provided
            if images:
                if not isinstance(images, list):
                    images = [images]
                for img in images:
                    parts.append(self._prepare_media_part(img))

            # Add audio parts if provided
            if audio:
                if not isinstance(audio, list):
                    audio = [audio]
                for ad in audio:
                    parts.append(self._prepare_media_part(ad))

            response = self.client.models.generate_content(
                model=self.model,
                contents=[{"role": "user", "parts": parts}],
            )

            return response.text or "(No response text received.)"

        except APIError as e:
            print(f"Gemini API Error: {e}")
            return f"An API error occurred: {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred while generating the response."
