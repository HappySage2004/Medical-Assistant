from dotenv import load_dotenv
load_dotenv()

#============================= Testing NL2Sql analyzer ===============================

# import os, time
# import datetime
# from custom_llm_services.gemini_llm_service import GeminiClient
# from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient

# from video_processor import extract_video_context

# import crewai
# from crewai import Agent, Task, Crew
# from crewai_tools import SerperDevTool, NL2SQLTool

# # Create connection URI
# db_uri = "mssql+pyodbc://Team_24:No2&5B8B3A0F@MER-SSIS-TRAIN.mipl.com/Agentic_AI_Hackathon?driver=ODBC+Driver+17+for+SQL+Server&autocommit=True"
# nl2sql = NL2SQLTool(db_uri=db_uri)

# azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.1,
#                              api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
#                              endpoint    =  os.getenv("AZURE_ENDPOINT"),
#                              api_version =  os.getenv("AZURE_API_VERSION"))


# agent = Agent(
#     role = "SQL Metrics Analyzer",
#     goal = "Use the information stored in the given SQL databases to answer user queries regarding important metrics like \
#             sales performance, operational efficiency and people performance. Use the schema information to accurately construct \
#             SQL queries for any user question.",
#     backstory = (
#         "You are an expert in SQL and business analytics. You understand complex database schemas "
#         "and can translate natural language questions into optimized SQL queries. "
#         "Always use the 'sql_query' parameter when passing the query to the NL2SQLTool.\n\n"
        
#         "You have access to the following database tables and their columns:\n\n"

#         # ------------------ CUSTOMER TRANSACTIONS ------------------
#         "[dbo].[customer_transactions]: Contains details of all customer transactions.\n"
#         "Columns:\n"
#         "- Transaction_ID (bigint): Unique identifier for each transaction.\n"
#         "- Customer_ID (bigint): Unique identifier for each customer.\n"
#         "- Store (varchar): Name or location code of the store.\n"
#         "- Age (bigint): Age of the customer.\n"
#         "- Gender (varchar): Gender of the customer.\n"
#         "- Income (varchar): Income group or classification.\n"
#         "- Date (varchar): Full date of the transaction.\n"
#         "- Year (bigint), Month (varchar), Day (bigint), Time (time): Transaction time details.\n"
#         "- Total_Quantity (bigint): Total number of units purchased.\n"
#         "- Unit_Price (float): Price per unit.\n"
#         "- Total_Amount (float): Total value of the transaction.\n"
#         "- Product (varchar): Purchased product name.\n"
#         "- Product_Category (varchar): Product category or classification.\n"
#         "- Customer_Feedback (varchar): Customer feedback or rating.\n"
#         "- Payment_Method (varchar): Mode of payment (Cash, Card, Digital Wallet).\n\n"

#         # ------------------ EMPLOYEE SHIFTS ------------------
#         "[dbo].[employee_shifts]: Records employee shift attendance and working hours.\n"
#         "Columns:\n"
#         "- Employee_ID (varchar): Unique identifier of employee.\n"
#         "- Name (varchar): Full name of the employee.\n"
#         "- Store (varchar): Store location or branch.\n"
#         "- Assigned_Role (varchar): Job title or position (Cashier, Manager, etc.).\n"
#         "- Date (varchar): Date of the recorded shift.\n"
#         "- Month (varchar): Month of the recorded work shift.\n"
#         "- Clock_In (time): Time employee started the shift.\n"
#         "- Clock_Out (time): Time employee ended the shift.\n"
#         "- Shift_Hours (float): Total hours worked during the shift.\n\n"

#         # ------------------ EMPLOYEE INFO ------------------
#         "[dbo].[employee_info]: Contains employee personal and performance information.\n"
#         "Columns:\n"
#         "- Employee_ID (varchar): Unique identifier of employee.\n"
#         "- Name (varchar): Employee’s full name.\n"
#         "- Store (varchar): Store branch where the employee works.\n"
#         "- Assigned_Role (varchar): Designation or position (Cashier, Supervisor, etc.).\n"
#         "- Hire_Date (varchar): Date when the employee joined the organization.\n"
#         "- Tenure_Years (float): Duration of service in years.\n"
#         "- Overall_Employee_Performance_Rating (bigint): Performance evaluation score.\n\n"

#         # ------------------ STORE INFO ------------------
#         "[dbo].[store_info]: Contains store-level location and reference details.\n"
#         "Columns:\n"
#         "- Store_ID (varchar): Unique identifier of the store.\n"
#         "- Full_Address (varchar): Physical address (street, city, postal code).\n"
#         "- Geo_Location_ID (varchar): Geographic code linking the store to a region.\n\n"

#         "Use joins appropriately:\n"
#         "- 'Store' in [customer_transactions], [employee_info], and [employee_shifts] "
#         "can be linked with 'Store_ID' in [store_info] for store-level details.\n"
#         "- 'Employee_ID' links [employee_info] and [employee_shifts].\n"
#         "- 'Store' can be used to aggregate transaction and employee metrics per branch.\n\n"
#     ),
#     tools = [nl2sql],
#     llm=azureopenai_llm,
#     verbose = True
# )

# task = Task(
#     description = (
#         "Find the following metrics from the database: Sales Performance, Operational Efficiency, People Performance for only {store}."
#         "Also write one small 100 word paragraph on interpreting these insights and another small paragraph on ways to improve the metrics. "
#     ),
#     expected_output = '''
#                             A JSON structured output containing the answer to each of the asked question.
#                             {
#                             "insights_para":"A paragraph (about 100 words) on insights that can be interpreted from the metrics",
#                             "improvements_para":"A paragraph (about 100 words) on potential improvements that can be made to improve the metrics",
#                             "total sales": "total sales for {store}",
#                             "MoM sales growth":"Sales growth compared to last month. Current month is {month}",
#                             "Average Order Value (AOV)":"Total_Amount / COUNT(Transaction_ID)",
#                             "Employee Utilization":"Shift_Hours / Store Total Hours",
#                             "Average employee rating":"Average employee rating",
#                             }
#                             Only return the above JSON block. Do not include any additional explanation or text outside the JSON.
#                             ''',
#     agent=agent,
# )

# inputs = {"store":"Store1", "month":str(datetime.datetime.now().month)}
# crew = Crew(agents=[agent], tasks=[task])
# start = time.time()
# result = crew.kickoff(inputs=inputs)
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result.raw)


# ================================ Fetching Online Reviews ===============================================
from serpapi import GoogleSearch
import os

import json
with open("local_db/store_reviews/store_ids.json", "r") as f:
    data = json.load(f)

DESIRED_KEYS = ['rating','snippet']
prev_page_token = ""

for store in data:
    print(data[store]["data_id"])
    reviews = []
    prev_page_token = "CAESY0NBRVFDQnBFUTJwRlNVRlNTWEJEWjI5QlVEZGZURUpNVTBOZlgxOWZSV2hFTW10RlNuRlpPRjlEYlZGeVUySnRXVUZCUVVGQlIyZHVPVEpoWTBOaFNVbFFhR1pSV1VGRFNVRQ=="
    for i in range(0,10):
        params = {
        "engine": "google_maps_reviews",
        "hl": "en",
        "data_id": data[store]["data_id"],
        "num": "20",
        "sort_by": "qualityScore",
        "next_page_token": prev_page_token,
        "api_key": os.getenv("SERP_API_KEY")
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        new_result = [ {
                        key: original_object[key]
                        for key in DESIRED_KEYS
                        if key in original_object # Ensure the key exists before trying to access it
                        } 
                    for original_object in results["reviews"] ]
        reviews.extend(new_result)
        prev_page_token = results["search_parameters"]["next_page_token"]
    
    with open(f"local_db\store_reviews\{store}_reviews.json", 'w') as f:
        json.dump(reviews, f)


# ================================ Fetching Image Reviews ===============================================

# import os, time, asyncio
# import json
# from base64 import b64encode
# from pathlib import Path
# from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient
# from video_processor import extract_video_context

# gpt_nano = AzureOpenAIClient()

# start = time.time()
# vid_ids = []
# vid_reviews = []
# directory_path = Path('Output_videos') 
# all_paths = [item for item in directory_path.iterdir()]
# for vid in all_paths:
#     list = str(vid).split('-')[0].split('\\')
#     print(list)
#     if list[-1] == "Store5":
#         frames, audio = extract_video_context(str(vid) ,"azure")
#         result = gpt_nano.get_response( query="You are given a video of a retail store. Analyze the frames and audio carefully and write a single paragraph description (about 200 words) of the video \
#                                             While writing the description focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
#                                             misplaced inventory, empty shelves.", 
#                                         images= frames)
                                        
#         with open(frames[0], "rb") as f:
#             encoded = b64encode(f.read()).decode("utf-8")
#             print(encoded[-100:-20:5])

#         vid_data = {"vid_id": encoded[-100:-20:5],
#                     "insights" : result}
#         vid_ids.append(encoded[-100:-20:5])
#         vid_reviews.append(vid_data)
    
# reviews = {"vid_ids":vid_ids,
#           "vid_reviews":vid_reviews}
# with open(f"local_db/video_reviews/Store5_video_reviews.json", 'w') as f:
#     json.dump(reviews, f)
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)




# ================================ Fetching Image Reviews ===============================================

# import os, time, asyncio
# import json
# from base64 import b64encode
# from pathlib import Path
# from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient
# from video_processor import extract_video_context

# gpt_nano = AzureOpenAIClient()

# start = time.time()
# vid_ids = []
# vid_reviews = []
# directory_path = Path('Output_videos') 
# all_paths = [item for item in directory_path.iterdir()]
# for vid in all_paths:
#     list = str(vid).split('-')[0].split('\\')
#     print(list)
#     if list[-1] == "Store5":
#         frames, audio = extract_video_context(str(vid) ,"azure")
#         result = gpt_nano.get_response( query="You are given a video of a retail store. Analyze the frames and audio carefully and write a single paragraph description (about 200 words) of the video \
#                                             While writing the description focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
#                                             misplaced inventory, empty shelves.", 
#                                         images= frames)
                                        
#         with open(frames[0], "rb") as f:
#             encoded = b64encode(f.read()).decode("utf-8")
#             print(encoded[-100:-20:5])

#         vid_data = {"vid_id": encoded[-100:-20:5],
#                     "insights" : result}
#         vid_ids.append(encoded[-100:-20:5])
#         vid_reviews.append(vid_data)
    
# reviews = {"vid_ids":vid_ids,
#           "vid_reviews":vid_reviews}
# with open(f"local_db/video_reviews/Store5_video_reviews.json", 'w') as f:
#     json.dump(reviews, f)
# end = time.time()
# print("Time taken to get response : ", end-start, "s")
# print(result)


# ================================ Fetching Store Alerts ===============================================

import os, time, asyncio
import json
from base64 import b64encode
from pathlib import Path
from custom_llm_services.azureopenai_llm_service import AzureOpenAIClient
from video_processor import extract_video_context

def realtime_store_alerts(all_paths = None, type:str = None):
    gpt_nano = AzureOpenAIClient()

    start = time.time()
    img_issues = []
    directory_path = Path('Images\Store 5') 
    all_paths = [item for item in directory_path.iterdir()]
    for img in all_paths:
        # frames, audio = extract_video_context(str(img) ,"azure")
        result = gpt_nano.get_response( query="You are given a Image of a retail store. Analyze the Images carefully and find problems that may require alerts. \
                                            In the output give only a list of strings having either one or more elements from the following list : \
                                            [empty shelves, spilled aisles, long queues on billing counters, no issues]", 
                                        images= str(img))
                                        
        with open(img, "rb") as f:
            encoded = b64encode(f.read()).decode("utf-8")
            print(encoded[-100:-20:5], end = " || ")

        img_data = {"img_id": encoded[-100:-20:5],
                    "issues" : result}
        img_issues.append(img_data)
        
    with open(f"local_db/store_alerts/Store5_images_issues.json", 'w') as f:
        json.dump(img_issues, f)

    vid_issues = []
    directory_path = Path('Output_videos') 
    all_paths = [item for item in directory_path.iterdir()]
    for vid in all_paths:
        list = str(vid).split('-')[0].split('\\')
        print(list)
        if list[-1] == "Store5":
            frames, audio = extract_video_context(str(vid) ,"azure")
            result = gpt_nano.get_response( query="You are given a Vido of a retail store. Analyze the frames carefully and find problems that may require alerts. \
                                            In the output give only a list of strings having either one or more elements from the following list : \
                                            [empty shelves, spilled aisles, long queues on billing counters, no issues]", 
                                            images= frames)
                                            
            with open(frames[0], "rb") as f:
                encoded = b64encode(f.read()).decode("utf-8")
                print(encoded[-100:-20:5])

            vid_data = {"vid_id": encoded[-100:-20:5],
                        "issues" : result}
            print(vid_data["issues"])
            vid_issues.append(vid_data)
        
    with open(f"local_db/store_alerts/Store5_videos_issues.json", 'w') as f:
        json.dump(vid_issues, f)
    end = time.time()
    print("Time taken to get response : ", end-start, "s")