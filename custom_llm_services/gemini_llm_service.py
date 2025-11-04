# import os
# from google import genai
# from google.genai.errors import APIError

# class GeminiClient:

#     def __init__(self, api_key=None):
#         key = api_key or os.getenv("GEMINI_API_KEY")
#         if not key:
#             raise ValueError("API key must be provided or set in the GEMINI_API_KEY environment variable.")

#         # Initializing the client
#         self.client = genai.Client(api_key=key)


#     def get_response(self, query: str) -> str:
#         """
#         Generates content from the Gemini model based on a user query.
#         Args:
#             query: The prompt to send to the model.
#         Returns:
#             The model's text response, or an error message if the call fails.
#         """
            
#         try:
#             response = self.client.models.generate_content(
#                 model="gemini-2.5-flash-lite",
#                 contents=query,
#             )

#             return response.text

#         except APIError as e:
#             # Handle specific API errors (e.g., invalid key, rate limiting)
#             print(f"Gemini API Error: {e}")
#             return f"An API error occurred {e}"
#         except Exception as e:
#             # Handle unexpected errors
#             print(f"An unexpected error occurred: {e}")
#             return "An unexpected error occurred while generating the response."

import os
from google import genai
from google.genai.errors import APIError
from base64 import b64encode

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


    def _prepare_image_part(self, image):
        """
        Internal helper to prepare an image part for the Gemini API.
        Accepts either a file path (str) or a dict with {data, mime_type}.
        """
        if isinstance(image, str):
            # assume it's a local file path
            mime_type = "image/jpeg" if image.lower().endswith(("jpg", "jpeg")) else "image/png"
            with open(image, "rb") as f:
                data = f.read()
            return {"inline_data": {"mime_type": mime_type, "data": data}}

        elif isinstance(image, dict) and "data" in image:
            # already a base64 or raw binary dict
            return {"inline_data": {
                "mime_type": image.get("mime_type", "image/jpeg"),
                "data": image["data"],
            }}

        else:
            raise ValueError("Invalid image format. Must be a file path or dict with 'data' and 'mime_type'.")


    def get_response(self, query: str, images=None) -> str:
        """
        Generates content from the Gemini model based on text and optional image inputs.
        Args:
            query: Text prompt to send to the model.
            images: Optional list of image file paths or base64 dicts.
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
                    parts.append(self._prepare_image_part(img))

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
