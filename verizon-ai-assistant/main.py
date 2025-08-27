# main.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langgraph_supervisor import create_supervisor

# Import agent builders
from agents.customer_context_agent import build_customer_context_agent
from agents.document_retrieval_agent import build_document_retrieval_agent
from agents.sales_intelligence_agent import build_sales_intelligence_agent
from agents.tool_using_agent import build_tool_using_agent

# Load environment variables
# load_dotenv()
# if "GOOGLE_API_KEY" not in os.environ:
#     raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")

from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()


print("Initializing AI model...")
# Using a powerful model for the supervisor is key
llm = ChatVertexAI(model="gemini-2.0-flash-001", temperature=0)

print("Building specialized agents...")
customer_agent = build_customer_context_agent(llm)
document_agent = build_document_retrieval_agent(llm)
sales_agent = build_sales_intelligence_agent(llm)
tool_agent = build_tool_using_agent(llm)

# List of all agents for the supervisor
all_agents = [customer_agent, document_agent, sales_agent, tool_agent]

print("Creating supervisor workflow...")
supervisor_prompt = """You are the 'Orchestrator', an intelligent AI supervisor for Verizon customer service.
Your role is to coordinate multiple specialist agents to provide comprehensive, insightful responses to customer service queries.

Available Specialist Agents:
1. customer_context_expert:
   - Gets customer profiles, history, and current plans
   - Use for any customer-specific information needs
   
2. document_retrieval_expert:
   - Accesses policy manuals and product documentation
   - Use for finding official information about policies, products, and procedures
   
3. sales_intelligence_expert:
   - Provides sales strategies and successful pitch examples
   - Use for sales and retention-related advice
   
4. business_tool_expert:
   - Checks service availability and generates recommendations
   - Use for technical feasibility checks and product suggestions

Your Workflow:
1. Analyze the Query:
   - Break down complex queries into information needs
   - Identify which agents need to be consulted

2. Gather Information:
   - Call relevant agents in a logical sequence
   - Pass context between agents when needed
   Example: For a sales opportunity, first get customer context, then check service availability, then get sales advice

3. Synthesize Response:
   - Combine information from all agents
   - Present a coherent, detailed response
   - Include specific details and actionable insights

4. Format Output:
   Structure your response clearly with sections like:
   - Customer Information (when relevant)
   - Technical Details (when relevant)
   - Recommendations/Next Steps
   - Supporting Policies/Documentation

Examples of Multi-Agent Queries:
1. "Tell me about customer 74829's upgrade options"
   - Use customer_context_expert for current plan
   - Use business_tool_expert for available services
   - Use sales_intelligence_expert for pitch strategy

2. "Can Jane Doe get fiber, and what's our installation policy?"
   - Use business_tool_expert for feasibility
   - Use document_retrieval_expert for installation details

Remember:
- Always gather complete context before making recommendations
- Cross-reference information between agents when relevant
- Provide specific, actionable insights
- Cite relevant policies or documentation
- Make your response comprehensive but easy to read
"""

workflow = create_supervisor(
   agents=all_agents,
   model=llm,
   prompt=supervisor_prompt,
   output_mode="full_history", # Only show the final synthesized response
   supervisor_name="orchestrator",
   include_agent_name=False,
   add_handoff_back_messages=True
   
)

# Compile the workflow into a runnable app
app = workflow.compile(checkpointer=checkpointer)
print("\n✅ AI Assistant is ready. Type your query below or 'exit' to quit.")
def main(app):
    while True:
        query = input("Customer Service Agent> ")
        if query.lower() == "exit":
            break
        if not query:
            continue
        config = {"configurable": {"thread_id": "1"}}

        # Invoke the supervisor with the user's query
        result = app.invoke({
            "messages": [{"role": "user", "content": query}],
           
        } ,config= config)

        # Print the final response from the supervisor
        final_response = result['messages'][-1]
        print("\nAI Assistant Response:")
        print(final_response.content)
        print("-" * 50 + "\n")

graph = (workflow.compile(checkpointer=checkpointer))

if __name__ == "__main__":
    main(app)
