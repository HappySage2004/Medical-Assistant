from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from crewai_tools import RagTool

def split_content(video_insights:str):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200,separators=["\n\n","\n"," "])
    splitted_documents = splitter.split_text(video_insights)

    return splitted_documents

def index_content_gemini(content):
    # Create a RAG tool with custom configuration
    config = {
        "vectordb": {
            "provider": "qdrant",
            "config": {
                "collection_name": "my-collection"
            }
        },
        "embedding_model": {
            "provider": "google-generativeai",
            "config": {
                "model": "gemini-embedding-001"
            }
        }
    }

    rag_tool = RagTool(config=config, summarize=True)
    return rag_tool

def create_FAISS_store():
    pass

if __name__ == "__main__":
    rag_tool = index_content_gemini(" ")
    rag_tool.add(data_type="text", content = "My name is Aaryan." )
    