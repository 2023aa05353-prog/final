# agents/sales_intelligence_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools.sales_tools import get_successful_sales_examples
from langchain_google_vertexai import ChatVertexAI
def build_sales_intelligence_agent(llm: ChatVertexAI):
    agent_prompt = """You are the 'Sales Intelligence Expert'.
    Your role is to help the customer service agent sell and retain customers.
    You have access to a database of successful sales pitches.
    You must analyze the user's request, which should contain a customer profile summary, and then use your tool to find relevant examples.
    Based on the examples, formulate a concise, actionable sales pitch or talking point.
    You must not access general company policies or perform technical checks."""

    tools = [get_successful_sales_examples]
    
    return create_react_agent(
        model=llm,
        tools=tools,
        name="sales_intelligence_expert",
        prompt=agent_prompt
    )
