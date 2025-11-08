from dotenv import load_dotenv
load_dotenv()

import os, time
from custom_llm_services.gemini_llm_service import GeminiClient
from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient

from video_processor import extract_video_context

import crewai
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool


# gemini = GeminiClient()
# start = time.time()
# frames, audio = extract_video_context("videos/video1.mp4", "gemini")
# result = gemini.get_response( query="Describe what you see in this video.", 
#                               images= frames,
#                               audio = audio )
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)

# print("="*100)

# gpt_nano = AzureOpenAIClient()
# start = time.time()
# frames, audio = extract_video_context("videos/video1.mp4" ,"azure")
# result = gpt_nano.get_response( query="Describe what you see in this video.", 
#                               images= frames,
#                               audio = audio )
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)



# gemini_llm = crewai.LLM(model="gemini/gemini-2.5-flash", temperature=0.3)
azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))


agent = Agent(
    role = "Online Review Analyzer",
    goal = "F",
    backstory = "",
    tools = [SerperDevTool()],
    llm=azureopenai_llm,
    verbose = True
)

task = Task(
    description = "Find online reviews of store {store_name} from the web. Try taking information\
                   from sources that have trusted reviews.",
    expected_output = "[Phone Name]\n[price]\n[processor]\n[camera specs]\n[screen size]\n \
                       [battery life]\n[waterproofing]\n Follow the above format for all the phones",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
start = time.time()
result = crew.kickoff()
end = time.time()
print("Time taken to get response : ", end-start, "s")
print(result.raw)

# from vector_store import index_content_gemini
# rag_tool = index_content_gemini(" ")
# rag_tool.add("My name is Aaryan. I am a Data Scientist as Accordion. \
#               B.Tech from IIT KGP in mining engineering.")

# agent1 = Agent(
#                 role = "Lead Generator",
#                 goal = "Find people from particualr professions whom I can target \
#                         to sell my products.",
#                 backstory = "",
#                 tool = [rag_tool],
#                 llm = gemini_llm,
#                 verbose = True
#               )

# task1 = Task(
#                 description = "Find details of people whom I can sell my data science course",
#                 expected_output = "All avaialable details of a person in points",
#                 agent = agent1
#             )

# crew = Crew(agents=[agent1], tasks=[task1])
# start = time.time()
# result = crew.kickoff()
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result.raw)