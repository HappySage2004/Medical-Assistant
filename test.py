from dotenv import load_dotenv
load_dotenv()

import os, time
from custom_llm_services.gemini_llm_service import GeminiClient
from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient

from video_processor import extract_video_context

import crewai
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, NL2SQLTool

# Create connection URI
db_uri = "mssql+pyodbc://Team_24:No2&5B8B3A0F@MER-SSIS-TRAIN.mipl.com/Agentic_AI_Hackathon?driver=ODBC+Driver+17+for+SQL+Server&autocommit=True"
nl2sql = NL2SQLTool(db_uri=db_uri)

azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))


agent = Agent(
    role = "SQL Analyzer agent",
    goal = "Query database using natural language",
    backstory = "Expert at querying databases. Always pass natural language questions using the 'sql_query' parameter.",
    tools = [nl2sql],
    llm=azureopenai_llm,
    verbose = True
)

task = Task(
    description = (
        "Find the total revenue of each store. Also mention the store address for all the stores."
        "The table having transactions is [dbo].[customer_transactions] and the use the columns Store and Total_Amount for this task."
        "The table having store information is [dbo].[store_info] and the use the column Full Address"
        "Use the NL2SQLTool with the parameter name 'sql_query' to execute the SQL query."
    ),
    expected_output = "list of store names and total revenue.",
    agent=agent,
)

crew = Crew(agents=[agent], tasks=[task])
start = time.time()
result = crew.kickoff()
end = time.time()
print("Time taken to get response : ", end-start, "s")
print(result.raw)

