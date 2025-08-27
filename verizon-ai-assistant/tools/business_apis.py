# tools/business_apis.py
import json
from langchain_core.tools import tool

@tool
def check_service_feasibility(customer_id: str) -> str:
    """
    Checks if the 'Pro' Fiber Plan is available at a customer's address.
    Requires the customer_id to look up their address.
    """
    # This is a mock tool. In a real scenario, it would call an API.
    # For this example, we'll say it's available for Jane Doe (74829).
    if customer_id == "74829":
        return json.dumps({
            "is_feasible": True,
            "max_speed_mbps": 1000,
            "notes": "Fiber to the home available."
        })
    return json.dumps({
        "is_feasible": False,
        "notes": "Service not available at the customer's address."
    })

@tool
def get_product_recommendations(customer_id: str) -> str:
    """
    Suggests products based on a customer's profile.
    Requires the customer_id.
    """
    if customer_id == "74829": # Jane Doe shows interest in premium services
        return json.dumps({
            "recommendations": [
                {
                    "product_id": "bundle_pro_01",
                    "name": "Pro Fiber + TV Bundle",
                    "reason": "Upgrade from basic internet, aligns with premium interest."
                },
                {
                    "product_id": "fiber_pro_only",
                    "name": "Pro Fiber Internet",
                    "reason": "Direct performance upgrade for heavy usage."
                }
            ]
        })
    return json.dumps({"recommendations": []})
