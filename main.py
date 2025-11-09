from dotenv import load_dotenv
load_dotenv()

import os, time
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

gpt_nano = AzureOpenAIClient()
start = time.time()
frames, audio = extract_video_context("Output_videos\Store1-01-10-2024.mp4" ,"azure")
result = gpt_nano.get_response( query="You are given a video of a retail store. Analyze the frames and audio carefully and write a single paragraph description (about 200 words) of the video \
                                        While writing the description focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
                                        misplaced inventory, empty shelves.", 
                              images= frames)
                              
end = time.time()
print("Time taken to get response : ", end-start, "s")
print(result)



# azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
#                              api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
#                              endpoint    =  os.getenv("AZURE_ENDPOINT"),
#                              api_version =  os.getenv("AZURE_API_VERSION"))


# agent = Agent(
#     role = "Online Review Analyzer",
#     goal = "Your goal is to analyze reviews of mentioned stores and provide insights on them",
#     backstory = "",
#     tools = [SerperDevTool()],
#     llm=azureopenai_llm,
#     verbose = True
# )

# task = Task(
#     description = "Find online reviews of store {store_name} at {store_location} from the web. Try taking information\
#                    from sources that have trusted reviews.",
#     expected_output = "[sample review 1], [sample review 2], .... upto 5 reviews from real users.",
#     agent=agent,
# )

# inputs = {"store_name" : "Sainsbury's", "store_location": "Harrow Manorway, Abbey Wood, London SE2 9NU, United Kingdom" }
# crew = Crew(agents=[agent], tasks=[task])
# start = time.time()
# result = crew.kickoff(inputs= inputs)
# end = time.time()
# print("Time taken to get response : ", end-start, "s")