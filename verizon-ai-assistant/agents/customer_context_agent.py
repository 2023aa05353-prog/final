# agents/customer_context_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from tools.crm_tools import get_customer_details, get_customer_interaction_history

def build_customer_context_agent(llm: ChatVertexAI):
    agent_prompt = """You are the 'Customer Context Expert'.
    Your sole purpose is to retrieve information about a customer from the CRM using the tools provided.
    You can get a customer's full profile details and their past interaction history.
    You must not answer questions about policies, sales, or technical feasibility.
    Strictly use the tools available to you to answer questions."""

    tools = [get_customer_details, get_customer_interaction_history]
    
    return create_react_agent(
        model=llm,
        tools=tools,
        name="customer_context_expert",
        prompt=agent_prompt
    )
