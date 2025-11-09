from typing import Union
from fastapi import FastAPI,Response, Body, Header, HTTPException
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()

import os, time
import datetime
import json
import crewai
from crewai import Agent, Task, Crew
from crewai_tools import NL2SQLTool

app = FastAPI()
app_version = "/v1"

@app.get(app_version + "/health_check")
def read_root():
    return {"Hello": "World"}

@app.get(app_version + "/stores_list")
def read_root():
    return {
        "stores":  [
                    {"id": "Store1", "name": "Store 1"},
                    {"id": "Store2", "name": "Store 2"},
                    {"id": "Store3", "name": "Store 3"},
                    {"id": "Store4", "name": "Store 4"},
                    {"id": "Store5", "name": "Store 5"},
                   ]
    }

@app.post(app_version + "/fetch_mi_for_oniline_reveiws", status_code=200)
def read_root(store_id:str | None = Body(default=None, convert_underscores=False)):

    start = time.time()
    azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))

    agent = Agent(
        role = "Online Review Analyzer",
        goal = "Your goal is to analyze reviews of a given store and provide insights on them. \
                Provide a single paragraph of insights(about 100 words) and another paragraph on improvement suggestions(about 100 words). \
                While writing the insights focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
                product availability, ease of finding desired items, parking, and Discount offers (like nectar card). \
                You also need to provide an overall sentiment score that combines the effect of the individual parameters.",
        backstory = "",
        llm=azureopenai_llm,
        verbose = True
    )

    task = Task(
        description = "Provide a single paragraph of insights(about 100 words) and another paragraph on improvement suggestions(about 100 words). \
                       While writing the insights focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
                       product availability, ease of finding desired items, parking, and Discount offers (like nectar card). \
                       You also need to provide an overall sentiment score that combines the effect of the individual parameters.\n \
                       STORE REVIEWS: \n \
                       {reviews_json}",
        expected_output =  '''
                            A JSON structured output containing the answer to each of the asked question.
                            {
                            "insights_para":"A paragraph (about 100 words) on insights dervied from the reviews",
                            "improvements_para":"A paragraph (about 100 words) on potential improvements that can be made to improve customer experience",
                            "Cleanliness_score":"a single digit score from 1-5 based on how clean the stores are according to the reviews.",
                            "Staff_behaviour_score":"a single digit score from 1-5 based on how well the staff at the store behave with the customers according to the reviews.",
                            "Product_availability_score":"a single digit score from 1-5 based on how satisfied the customers are with the variety of product offerings according to the reviews.",
                            "Parking_score":"a single digit score from 1-5 based on how the customers view the parking facility according to the reviews.",
                            "Discount":"a single digit score from 1-5 based on how content the users are with the discounts according to the reviews.",
                            "overall_sentiment" : "a single word out of [positive, negative, neutral] based on what you think is the overall opinion of the custmers on the store based on all the reviews."
                            }
                            Only return the above JSON block. Do not include any additional explanation or text outside the JSON.
                            ''',
        agent=agent,
    )
    with open(f"local_db/store_reviews/{store_id}_reviews.json", "r") as f:
        reviews_json = json.load(f)
    inputs = {"reviews_json": str(reviews_json) }
    crew = Crew(agents=[agent], tasks=[task])
    
    result = crew.kickoff(inputs= inputs)
    print(result)
    result = json.loads(str(result))
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)



@app.post(app_version + "/fetch_mi_for_media_description", status_code=200)
def read_root(store_id:str | None = Body(default=None, convert_underscores=False)):

    start = time.time()
    azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))

    agent = Agent(
        role = "Media Description Analyzer",
        goal = "Your goal is to analyze image and video descriptions of a given store and provide insights on them. \
                Provide a single paragraph of insights(about 100 words) and another paragraph on improvement suggestions(about 100 words). \
                While writing the insights focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
                misplaced inventory, and empty shelves. \
                You also need to provide scores to the parameters from 1-5 with 1 being the worst score and 5 being the best.\
                You also need to provide an overall sentiment score that combines the effect of the individual parameters.",
        backstory = "",
        llm=azureopenai_llm,
        verbose = True
    )

    task = Task(
        description = "Provide a single paragraph of insights(about 100 words) and another paragraph on improvement suggestions(about 100 words). \
                       While writing the insights focus mainly on parameters like Staff Behaviour, Cleanliness, Queues(waiting time), \
                       misplaced inventory, and empty shelves. \
                       You also need to provide an overall sentiment score that combines the effect of the individual parameters.\n \
                       IMAGE REVIEWS: \n \
                       {image_reviews_json} \
                       VIDEO REVIEWS: \n \
                       {video_reviews_json}",
        expected_output =  '''
                            A JSON structured output containing the answer to each of the asked question.
                            {
                            "insights_para":"A paragraph (about 100 words) on insights dervied from the reviews",
                            "improvements_para":"A paragraph (about 100 words) on potential improvements that can be made to improve customer experience",
                            "Cleanliness_score":"a single digit score from 1-5 based on how clean the stores are according to the reviews.",
                            "Staff_behaviour_score":"a single digit score from 1-5 based on how well the staff at the store behave with the customers according to the reviews.",
                            "Waiting Queue_score":"a single digit score from 1-5 based on how satisfied the customers are with the variety of product offerings according to the reviews.",
                            "Misplaced_inventory_score":"a single digit score from 1-5 based on how the customers view the parking facility according to the reviews.",
                            "empty_shelves_score":"a single digit score from 1-5 based on how content the users are with the discounts according to the reviews.",
                            }
                            Only return the above JSON block. Do not include any additional explanation or text outside the JSON.
                            ''',
        agent=agent,
    )
    with open(f"local_db/image_reviews/{store_id}_image_reviews.json", "r") as f:
        image_reviews_json = json.load(f)["img_reviews"]
    with open(f"local_db/video_reviews/{store_id}_video_reviews.json", "r") as f:
        video_reviews_json = json.load(f)["vid_reviews"]
    inputs = {"image_reviews_json": str(image_reviews_json), "video_reviews_json": str(video_reviews_json) }
    crew = Crew(agents=[agent], tasks=[task])
    
    result = crew.kickoff(inputs= inputs)
    print(result)
    result = json.loads(str(result))
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)




@app.post(app_version + "/fetch_store_monitoring", status_code=200)
def read_root(b64:str | None = Body(default=None, convert_underscores=False)):
    start = time.time()
    with open(f"local_db/media_index.json", "r") as f:
        media_index_json = json.load(f)

    isPresent = False
    
    result = {}
    for store in media_index_json:
        for img in media_index_json[store]["images"]:
            if img == b64:
                with open(f"local_db/store_alerts/{store}_images_issues.json", "r") as f1:
                    issues = json.load(f1)
                    for imgx in issues:
                        if b64 == imgx["img_id"]:
                            result["issue"] = imgx["issues"]
                            isPresent = True
        for vid in media_index_json[store]["videos"]:
            if vid == b64:
                with open(f"local_db/store_alerts/{store}_videos_issues.json", "r") as f2:
                    issues = json.load(f2)
                    for vidx in issues:
                        if b64 == vidx["vid_id"]:
                            result["issue"] = vidx["issues"]
                            isPresent = True

    if isPresent == False:
        result["issue"] = "Sorry! this media file is currently not present in our database. Realtime media file processing is not yet implemented"
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)




@app.post(app_version + "/fetch_mi_for_structured_data", status_code=200)
def read_root(store_id:str | None = Body(default=None, convert_underscores=False)):

    start = time.time()
    # Create connection URI
    db_uri = "mssql+pyodbc://Team_24:No2&5B8B3A0F@MER-SSIS-TRAIN.mipl.com/Agentic_AI_Hackathon?driver=ODBC+Driver+17+for+SQL+Server&autocommit=True"
    nl2sql = NL2SQLTool(db_uri=db_uri)

    azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.1,
                                api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                                endpoint    =  os.getenv("AZURE_ENDPOINT"),
                                api_version =  os.getenv("AZURE_API_VERSION"))


    agent = Agent(
        role = "SQL Metrics Analyzer",
        goal = "Use the information stored in the given SQL databases to answer user queries regarding important metrics like \
                sales performance, operational efficiency and people performance. Use the schema information to accurately construct \
                SQL queries for any user question.",
        backstory = (
            "You are an expert in SQL and business analytics. You understand complex database schemas "
            "and can translate natural language questions into optimized SQL queries. "
            "Always use the 'sql_query' parameter when passing the query to the NL2SQLTool.\n\n"
            
            "You have access to the following database tables and their columns:\n\n"

            # ------------------ CUSTOMER TRANSACTIONS ------------------
            "[dbo].[customer_transactions]: Contains details of all customer transactions.\n"
            "Columns:\n"
            "- Transaction_ID (bigint): Unique identifier for each transaction.\n"
            "- Customer_ID (bigint): Unique identifier for each customer.\n"
            "- Store (varchar): Name or location code of the store.\n"
            "- Age (bigint): Age of the customer.\n"
            "- Gender (varchar): Gender of the customer.\n"
            "- Income (varchar): Income group or classification.\n"
            "- Date (varchar): Full date of the transaction.\n"
            "- Year (bigint), Month (varchar), Day (bigint), Time (time): Transaction time details.\n"
            "- Total_Quantity (bigint): Total number of units purchased.\n"
            "- Unit_Price (float): Price per unit.\n"
            "- Total_Amount (float): Total value of the transaction.\n"
            "- Product (varchar): Purchased product name.\n"
            "- Product_Category (varchar): Product category or classification.\n"
            "- Customer_Feedback (varchar): Customer feedback or rating.\n"
            "- Payment_Method (varchar): Mode of payment (Cash, Card, Digital Wallet).\n\n"

            # ------------------ EMPLOYEE SHIFTS ------------------
            "[dbo].[employee_shifts]: Records employee shift attendance and working hours.\n"
            "Columns:\n"
            "- Employee_ID (varchar): Unique identifier of employee.\n"
            "- Name (varchar): Full name of the employee.\n"
            "- Store (varchar): Store location or branch.\n"
            "- Assigned_Role (varchar): Job title or position (Cashier, Manager, etc.).\n"
            "- Date (varchar): Date of the recorded shift.\n"
            "- Month (varchar): Month of the recorded work shift.\n"
            "- Clock_In (time): Time employee started the shift.\n"
            "- Clock_Out (time): Time employee ended the shift.\n"
            "- Shift_Hours (float): Total hours worked during the shift.\n\n"

            # ------------------ EMPLOYEE INFO ------------------
            "[dbo].[employee_info]: Contains employee personal and performance information.\n"
            "Columns:\n"
            "- Employee_ID (varchar): Unique identifier of employee.\n"
            "- Name (varchar): Employee’s full name.\n"
            "- Store (varchar): Store branch where the employee works.\n"
            "- Assigned_Role (varchar): Designation or position (Cashier, Supervisor, etc.).\n"
            "- Hire_Date (varchar): Date when the employee joined the organization.\n"
            "- Tenure_Years (float): Duration of service in years.\n"
            "- Overall_Employee_Performance_Rating (bigint): Performance evaluation score.\n\n"

            # ------------------ STORE INFO ------------------
            "[dbo].[store_info]: Contains store-level location and reference details.\n"
            "Columns:\n"
            "- Store_ID (varchar): Unique identifier of the store.\n"
            "- Full_Address (varchar): Physical address (street, city, postal code).\n"
            "- Geo_Location_ID (varchar): Geographic code linking the store to a region.\n\n"

            "Use joins appropriately:\n"
            "- 'Store' in [customer_transactions], [employee_info], and [employee_shifts] "
            "can be linked with 'Store_ID' in [store_info] for store-level details.\n"
            "- 'Employee_ID' links [employee_info] and [employee_shifts].\n"
            "- 'Store' can be used to aggregate transaction and employee metrics per branch.\n\n"
        ),
        tools = [nl2sql],
        llm=azureopenai_llm,
        verbose = True
    )

    task = Task(
        description = (
            "Find the following metrics from the database: Sales Performance, Operational Efficiency, People Performance for only {store}."
            "Also write one small 100 word paragraph on interpreting these insights and another small paragraph on ways to improve the metrics. "
            "Use the NL2SQLTool with the parameter name 'sql_query' to execute the SQL query"
        ),
        expected_output = '''
                                A JSON structured output containing the answer to each of the asked question.
                                {
                                "insights_para":"A paragraph (about 100 words) on insights that can be interpreted from the metrics",
                                "improvements_para":"A paragraph (about 100 words) on potential improvements that can be made to improve the metrics",
                                "total sales": "total sales for {store}",
                                "MoM sales growth":"Sales growth compared to last month. Current month is {month}",
                                "Average Order Value (AOV)":"Total_Amount / COUNT(Transaction_ID)",
                                "Employee Utilization":"Shift_Hours / Store Total Hours",
                                "Average employee rating":"Average employee rating",
                                }
                                Only return the above JSON block. Do not include any additional explanation or text outside the JSON.
                                ''',
        agent=agent,
    )

    inputs = {"store": store_id, "month":str(datetime.datetime.now().month)}
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff(inputs=inputs)
    print(result)
    result = json.loads(str(result))
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)



@app.post(app_version + "/user_querying_for_single_store", status_code=200)
def read_root(store_id:str | None = Body(default=None, convert_underscores=False),
              query:str | None = Body(default=None, convert_underscores=False)):

    start = time.time()
    # Create connection URI
    db_uri = "mssql+pyodbc://Team_24:No2&5B8B3A0F@MER-SSIS-TRAIN.mipl.com/Agentic_AI_Hackathon?driver=ODBC+Driver+17+for+SQL+Server&autocommit=True"
    nl2sql = NL2SQLTool(db_uri=db_uri)

    azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))

    agent = Agent(
        role = "Retail Store Analyst",
        goal = "Your goal is to analyze online reviews, image and video descriptions of a given store, and summaries for SQL databases \
                to answer questions asked by your store manager for {store}. Hence only access data for {store}.\
                You will have access to the SQL tool to find information not present in the summaries. Use it only when required and not always. \
                After analyzing all the data prepare a concise answer. Use the NL2SQLTool with the parameter name 'sql_query' to execute the SQL query",
        backstory = "You are an analyst at the Sainsbury's retail. Your manager can ask you questions about the stores operations and \
                    continue his duties. You must provide extremely precise to the point answers to the queries and also give some insights if \
                    are any issues.",
        tools = [nl2sql],
        llm=azureopenai_llm,
        verbose = True
    )

    task = Task(
        description = "You have access to media insights (store videos and images) online reviews, as well as insights and metrics \
                       from the SQL database maintained by the store. Frame you answer to the manager's question using these resources.\
                       in addition you also have access to the SQL database using the SQL tool in case he wants some metrics not in the insights\
                       Use the tool only when you need extra information and not otherwise. Meticulously follow the instructions mentioned in the user query.\
                       USER QUESTION: {query} \
                       MEDIA INSIGHTS:\n\
                       {media_reviews_json} \
                       ONLINE REVIEWS:\n\
                       {online_reviews_json} \
                       DATABASE METRICS:\n\
                       {structured_reviews_json}",
        expected_output =  "A concise answer than can please the Store Manager.",
        agent=agent,
    )
    with open(f"local_db/consolidated_media_reviews.json", "r") as f:
        media_reviews_json = json.load(f)[store_id]
    with open(f"local_db/consolidated_online_reviews.json", "r") as f:
        online_reviews_json = json.load(f)[store_id]
    with open(f"local_db/consolidated_structured_output.json", "r") as f:
        structured_reviews_json = json.load(f)[store_id]


    inputs = {  
                "media_reviews_json": str(media_reviews_json), 
                "online_reviews_json": str(online_reviews_json),
                "structured_reviews_json": str(structured_reviews_json),
                "query" : query,
                "store": store_id
             }
    crew = Crew(agents=[agent], tasks=[task])
    
    result = crew.kickoff(inputs= inputs)
    print(result)
    result = {"response" : str(result)}
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)





@app.post(app_version + "/user_querying_for_all_store", status_code=200)
def read_root(query:str | None = Body(default=None, convert_underscores=False)):

    start = time.time()
    # Create connection URI
    db_uri = "mssql+pyodbc://Team_24:No2&5B8B3A0F@MER-SSIS-TRAIN.mipl.com/Agentic_AI_Hackathon?driver=ODBC+Driver+17+for+SQL+Server&autocommit=True"
    nl2sql = NL2SQLTool(db_uri=db_uri)

    azureopenai_llm = crewai.LLM(model="azure/Team24-GPT-4.1-mini-261100a543eaa0de3aa4", temperature=0.2,
                             api_key     =  os.getenv("AZURE_OPENAI_API_KEY"),
                             endpoint    =  os.getenv("AZURE_ENDPOINT"),
                             api_version =  os.getenv("AZURE_API_VERSION"))

    agent = Agent(
        role = "Retail Store Analyst",
        goal = "Your goal is to analyze online reviews, image and video descriptions of a given store, and summaries for SQL databases \
                to answer questions asked by your store manager. Your store manager is a regional manager as well and hence has access to data from all the stores.\
                You will have access to the SQL tool to find information not present in the summaries. Use it only when required and not always. \
                After analyzing all the data prepare a concise answer. Use the NL2SQLTool with the parameter name 'sql_query' to execute the SQL query",
        backstory = "You are an analyst at the Sainsbury's retail. Your manager can ask you questions about the store's operations and \
                    continue his duties. You must provide extremely precise to the point answers to the queries and also give some insights if \
                    are any issues.",
        tools = [nl2sql],
        llm=azureopenai_llm,
        verbose = True
    )

    task = Task(
        description = "You have access to media insights (store videos and images) online reviews, as well as insights and metrics \
                       from the SQL database maintained by the store. Frame you answer to the manager's question using these resources.\
                       in addition you also have access to the SQL database using the SQL tool in case he wants some metrics not in the insights\
                       Use the tool only when you need extra information and not otherwise. Meticulously follow the instructions mentioned in the user query.\
                       USER QUESTION: {query} \
                       MEDIA INSIGHTS:\n\
                       {media_reviews_json} \
                       ONLINE REVIEWS:\n\
                       {online_reviews_json} \
                       DATABASE METRICS:\n\
                       {structured_reviews_json}",
        expected_output =  "A concise answer than can please the Store Manager.",
        agent=agent,
    )
    with open(f"local_db/consolidated_media_reviews.json", "r") as f:
        media_reviews_json = json.load(f)
    with open(f"local_db/consolidated_online_reviews.json", "r") as f:
        online_reviews_json = json.load(f)
    with open(f"local_db/consolidated_structured_output.json", "r") as f:
        structured_reviews_json = json.load(f)

    query = query.replace("'Store 1'", "'Store1'")
    query = query.replace("'Store 2'", "'Store2'")
    query = query.replace("'Store 3'", "'Store3'")
    query = query.replace("'Store 4'", "'Store4'")
    query = query.replace("'Store 5'", "'Store5'")
    query = query.replace("'store 1'", "'Store1'")
    query = query.replace("'store 2'", "'Store2'")
    query = query.replace("'store 3'", "'Store3'")
    query = query.replace("'store 4'", "'Store4'")
    query = query.replace("'store 5'", "'Store5'")

    inputs = {  
                "media_reviews_json": str(media_reviews_json), 
                "online_reviews_json": str(online_reviews_json),
                "structured_reviews_json": str(structured_reviews_json),
                "query" : query,
             }
    crew = Crew(agents=[agent], tasks=[task])
    
    result = crew.kickoff(inputs= inputs)
    print(result)
    result = {"response" : str(result)}
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)

@app.get(app_version + "/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post(app_version + "/consolidated_scorecard", status_code=200)
def read_root(store_id:str | None = Body(default=None, convert_underscores=False)):
    start = time.time()

    result = {}
    with open(f"local_db/consolidated_media_reviews.json", "r") as f:
        media_reviews_json = json.load(f)[store_id]
    with open(f"local_db/consolidated_online_reviews.json", "r") as f:
        online_reviews_json = json.load(f)[store_id]
    with open(f"local_db/consolidated_structured_output.json", "r") as f:
        structured_reviews_json = json.load(f)[store_id]

    result["Total Sales"] = str(structured_reviews_json["total sales"])
    result["MoM sales growth"] = str(structured_reviews_json["MoM sales growth"])
    result["Average employee rating"] = str(structured_reviews_json["Average employee rating"])
    result["overall_sentiment"] = str(online_reviews_json["overall_sentiment"])
    result["Staff_behaviour_score"] = str((int(online_reviews_json["Staff_behaviour_score"]) + int(media_reviews_json["Staff_behaviour_score"]))/2)
    result["Product_availability_score"] = str(online_reviews_json["Product_availability_score"])
    result["Cleanliness_score"] = str((int(online_reviews_json["Cleanliness_score"]) + int(media_reviews_json["Cleanliness_score"]))/2)
    result["Waiting Queue_score"] = str(media_reviews_json["Waiting Queue_score"])
    result["empty_shelves_score"] = str(media_reviews_json["empty_shelves_score"]) 
   
    end = time.time()
    print("Time taken for response : ", end-start ,"s")
    return JSONResponse(content=result, status_code=200)