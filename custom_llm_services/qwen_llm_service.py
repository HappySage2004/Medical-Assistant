import os
from huggingface_hub import InferenceClient

class QwenClient:

    def __init__(self, api_key:str = None):
        key = api_key or os.getenv("HF_TOKEN")
        if not key:
            raise ValueError("API key must be provided or set in the HF_TOKEN environment variable.")

        self.client = InferenceClient(provider="groq", api_key=os.environ["HF_TOKEN"])


    def get_response(self, query:str) -> str:
        completion = self.client.chat.completions.create(
            model="Qwen/QwQ-32B",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
        )

        return completion.choices[0].message.content