from dotenv import load_dotenv
load_dotenv()

import os, time
from custom_llm_services.gemini_llm_service import GeminiClient
from custom_llm_services.deepseekv3_llm_service import DeepseekClient

import crewai
from crewai import Agent, Task, Crew

gemini = GeminiClient()
start = time.time()
result = gemini.get_response("Describe what you see in this image.", images="images/download2.jpg")
end = time.time()
print("Time taken to get response : ", end-start, "s")
print(result)

# deepseek = DeepseekClient()
# start = time.time()
# result = deepseek.get_response(query="Explain quantum computing")
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)

# gemini_llm = crewai.LLM(model="gemini/gemini-2.5-flash-lite", temperature=0.3)

# agent = Agent(
#     role="Image Analyst",
#     goal="Describe or interpret images.",
#     backstory = "",
#     llm=gemini_llm,
#     multimodal=True,
# )

# task = Task(
#     description="Describe the contents of the image at: D:\\PROJECTS\\Medical Assistant\\images\\download1.jpg",
#     expected_output="Image type : [category of the image]\nDescription : [50 word description of the image]",
#     agent=agent,
# )

# crew = Crew(agents=[agent], tasks=[task])
# result = crew.kickoff()
# print(result.raw)
