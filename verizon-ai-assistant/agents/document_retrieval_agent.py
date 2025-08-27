# agents/document_retrieval_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools.retrieval_tools import search_business_documents
from langchain_google_vertexai import ChatVertexAI
def build_document_retrieval_agent(llm: ChatVertexAI):
    agent_prompt = """You are the 'Document Retrieval Expert'.
    You are an expert at searching and retrieving specific information from Verizon's internal documents, including policy manuals and product brochures.
    Use your search tool to find answers to questions about policies, terms and conditions, and product specifications.
    Do not access customer data or sales data. Provide the answer along with the source of the information."""

    tools = [search_business_documents]
    
    return create_react_agent(
        model=llm,
        tools=tools,
        name="document_retrieval_expert",
        prompt=agent_prompt
    )
