from langchain_nvidia_ai_endpoints import ChatNVIDIA

client = ChatNVIDIA(
  model="deepseek-ai/deepseek-v3.1",
  api_key="$API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC", 
  temperature=0.2,
  top_p=0.7,
  max_tokens=8192,
  extra_body={"chat_template_kwargs": {"thinking":True}},
)

for chunk in client.stream([{"role":"user","content":""}]):
  
    if chunk.additional_kwargs and "reasoning_content" in chunk.additional_kwargs:
      print(chunk.additional_kwargs["reasoning_content"], end="")
  
    print(chunk.content, end="")