import os
from huggingface_hub import InferenceClient

class DeepseekClient:
    
    def __init__(self, api_key:str = None):
        key = api_key or os.getenv("HF_TOKEN")
        if not key:
            raise ValueError("API key must be provided or set in the HF_TOKEN environment variable.")

        self.client = InferenceClient(provider="sambanova", api_key=os.environ["HF_TOKEN"])


    def get_response(self, query:str) -> str:
        completion = self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
        )

        return completion.choices[0].message.content