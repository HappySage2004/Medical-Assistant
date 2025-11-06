from dotenv import load_dotenv
load_dotenv()

import os, time
from custom_llm_services.gemini_llm_service import GeminiClient
from custom_llm_services.deepseekv3_llm_service import DeepseekClient

from video_processor import extract_video_context

import crewai
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool


# gemini = GeminiClient()
# start = time.time()
# frames, audio = extract_video_context("videos/video1.mp4")
# result = gemini.get_response( query="Describe what you see in this video.", 
#                               images= frames,
#                               audio = audio )
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)


gemini_llm = crewai.LLM(model="gemini/gemini-2.5-flash", temperature=0.3)
deepseek_llm = crewai.LLM(model="nvidia_nim/deepseek-ai/deepseek-r1", temperature=0.2)

deepseek_llm.call("What's a quadratic equation?")

agent = Agent(
    role = "Shopping Assistant",
    goal = "Assist the user in making purchase decisions by providing detailed  \
            up to date information about the products by searching from the internet. \
            Use the serper dev tool to access latest information from the web. Only make one tool call.",
    backstory = "",
    tools = [SerperDevTool()],
    llm=gemini_llm,
    verbose = True
)

task = Task(
    description = "Find 3 phones launched in October of 2025 from major brands",
    expected_output = "[Phone Name]\n[price]\n[processor]\n[camera specs]\n[screen size]\n \
                       [battery life]\n[waterproofing]\n Follow the above format for all the phones",
    agent=agent,
)

# crew = Crew(agents=[agent], tasks=[task])
# start = time.time()
# result = crew.kickoff()
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result.raw)