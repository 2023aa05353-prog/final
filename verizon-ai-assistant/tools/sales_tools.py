# tools/sales_tools.py
import json
from langchain_core.tools import tool

@tool
def get_successful_sales_examples(customer_profile_summary: str) -> str:
    """
    Retrieves examples of successful sales pitches for customers with a similar profile.
    Input should be a brief summary of the current customer's profile (e.g., 'interested in premium, low price sensitivity').
    """
    with open(r"C:\Users\infan\Documents\final\verizon-ai-assistant\data\mock_sales_history.json", "r") as f:
        sales_history = json.load(f)
    
    # Simple keyword matching for mock purposes
    relevant_examples = [
        example for example in sales_history 
        if "premium" in customer_profile_summary.lower() or "performance" in customer_profile_summary.lower()
    ]
    
    if relevant_examples:
        return json.dumps(relevant_examples)
    return "No similar sales examples found."
