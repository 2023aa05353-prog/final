# agents/tool_using_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools.business_apis import check_service_feasibility, get_product_recommendations
from langchain_google_vertexai import ChatVertexAI
def build_tool_using_agent(llm: ChatVertexAI):
    agent_prompt = """You are the 'Business Tool Expert'.
    You are a specialist in interacting with Verizon's internal APIs.
    You can check if a service plan is available at a customer's address and get product recommendations for a customer based on their ID.
    You must use the tools provided to answer the query. Do not attempt to answer questions outside of your tools' scope."""

    tools = [check_service_feasibility, get_product_recommendations]
    
    return create_react_agent(
        model=llm,
        tools=tools,
        name="business_tool_expert",
        prompt=agent_prompt
    )
