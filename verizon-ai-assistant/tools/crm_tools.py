# tools/crm_tools.py
import json
from langchain_core.tools import tool

def _load_crm_data():
    with open("/workspaces/miniconda/final/verizon-ai-assistant/data/mock_crm.json", "r") as f:
        return json.load(f)

@tool
def get_customer_details(customer_id: str) -> str:
    """
    Retrieves the full profile of a customer, including name, address, current plan, and profile notes.
    Use this to get a general overview of the customer.
    """
    crm_data = _load_crm_data()
    customer = crm_data.get(customer_id)
    if customer:
        return json.dumps(customer)
    return f"Error: Customer with ID '{customer_id}' not found."

@tool
def get_customer_interaction_history(customer_id: str) -> str:
    """
    Retrieves the past interaction history for a specific customer.
    Use this to understand past issues or inquiries.
    """
    crm_data = _load_crm_data()
    customer = crm_data.get(customer_id)
    if customer and "history" in customer:
        return json.dumps({"interaction_history": customer["history"]})
    return f"Error: No history found for customer ID '{customer_id}'."
