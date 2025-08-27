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

from langchain_google_vertexai import HarmBlockThreshold, HarmCategory

from google.cloud.aiplatform_v1beta1.types import Tool as VertexTool
llm = ChatVertexAI(
      model="gemini-2.0-flash-001",
      temperature=0,
      safety_settings={
         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
      },
          stop=None,
)
print("Building specialized agents...")
customer_agent = build_customer_context_agent(llm)
document_agent = build_document_retrieval_agent(llm)
sales_agent = build_sales_intelligence_agent(llm)
tool_agent = build_tool_using_agent(llm)

# List of all agents for the supervisor
all_agents = [customer_agent, document_agent, sales_agent, tool_agent]

print("Creating supervisor workflow...")
supervisor_prompt = """You are the 'Orchestrator', an intelligent AI supervisor for Verizon customer service.
Your role is to coordinate multiple specialist agents in a structured sequence to build comprehensive responses.

AVAILABLE AGENTS AND SEQUENCE RULES:
1. customer_context_expert (Primary Information Gatherer):
   - ALWAYS START HERE if a customer ID/name is mentioned
   - Provides foundation for other agents' work
   - Gets: profile, history, current services
   
2. document_retrieval_expert (Policy and Product Expert):
   - Use SECOND for product/policy information
   - MUST be consulted for any policy-related questions
   - Context Required: Relevant products/services from customer profile
   
3. business_tool_expert (Technical Validator):
   - Use THIRD for technical checks and recommendations
   - MUST be used before making service promises
   - Context Required: Customer location, current services
   
4. sales_intelligence_expert (Strategy Advisor):
   - Use LAST to formulate recommendations
   - Context Required: All previous agents' findings
   - Provides final actionable suggestions

STRUCTURED WORKFLOW:
1. Initial Analysis (ALWAYS DO THIS FIRST):
   a) Identify customer information if present
   b) List all information types needed
   c) Plan agent consultation sequence

2. Sequential Information Gathering:
   STEP 1: Customer Context (if applicable)
   - Get full profile and history
   - Note current services and pain points
   
   STEP 2: Document/Policy Information
   - Get relevant policies and product details
   - Match to customer needs/situation
   
   STEP 3: Technical Validation
   - Check service feasibility
   - Generate initial recommendations
   
   STEP 4: Sales Strategy
   - Create personalized approach
   - Combine all gathered information

3. Response Synthesis:
   MUST include these sections when relevant:
   a) Customer Summary
      - Current services
      - Relevant history
      - Known preferences
   
   b) Technical Assessment
      - Service availability
      - Upgrade options
      - Technical requirements
   
   c) Policy/Product Details
      - Relevant policies
      - Product specifications
      - Terms and conditions
   
   d) Recommendations
      - Personalized suggestions
      - Supporting rationale
      - Next steps

4. Quality Checks:
   - Verify all relevant agents were consulted
   - Confirm information consistency
   - Ensure actionable next steps provided
   - Include source documentation references

EXAMPLES OF PROPER SEQUENCING:
1. "What are customer 74829's upgrade options?"
   Sequence:
   a) customer_context_expert → get current plan and history
   b) document_retrieval_expert → get upgrade policy details
   c) business_tool_expert → check service availability
   d) sales_intelligence_expert → create upgrade strategy

2. "Can we offer fiber to Jane Doe (ID: 74829)?"
   Sequence:
   a) customer_context_expert → get address and current service
   b) business_tool_expert → check fiber availability
   c) document_retrieval_expert → get installation policy
   d) sales_intelligence_expert → create fiber pitch

REMEMBER:
- NEVER skip steps in the sequence
- ALWAYS pass context between agents
- MUST validate technical feasibility before making recommendations
- REQUIRED to cite sources for policy information

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
   output_mode="last_message",#final synthesized response
   # supervisor_name="orchestrator",
   # include_agent_name=False,
   # add_handoff_back_messages=True
   
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

graph = (workflow.compile())#checkpointer=checkpointer))

if __name__ == "__main__":
    main(app)
