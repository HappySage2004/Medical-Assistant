import os
from openai import AzureOpenAI
from openai import BadRequestError
from base64 import b64encode


class AzureOpenAIClient:
    """
    Wrapper for Azure OpenAI GPT-4.1 (Mini/Preview) that supports text, image, and audio inputs.
    Mirrors GeminiClient’s interface exactly.
    """

    def __init__(self, api_key=None, api_version=None, endpoint=None, model=None):
        # Load credentials and settings from environment if not explicitly passed
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = api_version or os.getenv("AZURE_API_VERSION")
        self.endpoint = endpoint or os.getenv("AZURE_ENDPOINT")
        self.model = model or os.getenv("MODEL_DEPLOYMENT")

        if not (self.api_key and self.api_version and self.endpoint and self.model):
            raise ValueError("Missing Azure OpenAI credentials or model deployment info.")

        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version
        )

    # ---------- Internal Helpers ---------- #

    def _prepare_media_part(self, file_path):
        """
        Prepare an image or audio file as a base64 inline data URL.
        Supports: jpg, jpeg, png, mp3, wav, ogg
        """
        ext = file_path.lower().split(".")[-1]
        mime_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "ogg": "audio/ogg",
        }
        mime_type = mime_map.get(ext)
        if not mime_type:
            raise ValueError(f"Unsupported file type: {ext}")

        with open(file_path, "rb") as f:
            encoded = b64encode(f.read()).decode("utf-8")

        # Azure expects images as "image_url" and audio as "input_audio"
        if mime_type.startswith("image/"):
            return {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{encoded}"}
            }
        elif mime_type.startswith("audio/"):
            return {
                "type": "input_audio",
                "input_audio": {"data": encoded, "format": ext}
            }

    # ---------- Core Response Function ---------- #

    def get_response(self, query: str, images=None, audio=None) -> str:
        """
        Generates a response from Azure OpenAI based on text + optional image/audio inputs.
        Args:
            query  : Text prompt to send to the model.
            images : Optional list of image file paths.
            audio  : Optional single or list of audio files.
        Returns:
            Model's textual response.
        """
        try:
            # Text part
            content = [{"type": "text", "text": query}]

            # Image parts
            if images:
                if not isinstance(images, list):
                    images = [images]
                for img in images:
                    content.append(self._prepare_media_part(img))

            # Audio parts
            if audio:
                if not isinstance(audio, list):
                    audio = [audio]
                for ad in audio:
                    content.append(self._prepare_media_part(ad))

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_completion_tokens=8192,
            )

            return response.choices[0].message.content.strip()

        except BadRequestError as e:
            print(f"Azure OpenAI API Error: {e}")
            return f"BadRequestError: {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred while generating the response."
