from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def split_content(video_insights:str):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200,separators=["\n\n","\n"," "])
    splitted_documents = splitter.split_text(video_insights)

    return splitted_documents

def create_FAISS_store():
    pass

