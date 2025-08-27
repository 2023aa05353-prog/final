# tools/business_apis.py
from typing import Optional, List, Dict, Any
import json
from datetime import datetime, timedelta
from langchain_core.tools import tool

# Mock database for demonstration
MOCK_CUSTOMERS = {
    "74829": {
        "name": "Jane Doe",
        "address": "123 Main St, Anytown, USA",
        "email": "jane.doe@email.com",
        "current_plan": "Internet Basic",
        "monthly_bill": 79.99,
        "join_date": "2024-11-01"
    },
    "99101": {
        "name": "John Smith",
        "address": "456 Oak Ave, Sometown, USA",
        "current_plan": "Pro Fiber + TV Bundle",
        "monthly_bill": 159.99,
        "join_date": "2023-05-15"
    }
}

MOCK_SERVICES = {
    "internet_basic": {"name": "Internet Basic", "base_price": 49.99},
    "pro_fiber": {"name": "Pro Fiber", "base_price": 89.99},
    "tv_basic": {"name": "Basic TV", "base_price": 50.00},
    "mobile_unlimited": {"name": "Unlimited Mobile", "base_price": 75.00}
}

@tool
def check_service_feasibility(customer_id: str, service_type: Optional[str] = "fiber") -> str:
    """
    Checks if specific services are available at a customer's address.
    Args:
        customer_id: The customer's ID
        service_type: Type of service to check (fiber, cable, 5g, etc.)
    """
    service_availability = {
        "74829": {
            "fiber": {"is_feasible": True, "max_speed_mbps": 1000, "notes": "Fiber to the home available"},
            "5g": {"is_feasible": True, "max_speed_mbps": 500, "notes": "5G Ultra Wideband available"},
            "cable": {"is_feasible": True, "max_speed_mbps": 200, "notes": "Cable service available"}
        },
        "99101": {
            "fiber": {"is_feasible": True, "max_speed_mbps": 2000, "notes": "Fiber to the home available"},
            "5g": {"is_feasible": False, "notes": "5G coverage not yet available"},
            "cable": {"is_feasible": True, "max_speed_mbps": 200, "notes": "Cable service available"}
        }
    }
    
    if customer_id not in service_availability:
        return json.dumps({
            "is_feasible": False,
            "notes": "Customer address not found in database"
        })
    
    return json.dumps(service_availability.get(customer_id, {}).get(service_type, {
        "is_feasible": False,
        "notes": f"Service type {service_type} not available"
    }))

@tool
def get_product_recommendations(customer_id: str, context: Optional[str] = None) -> str:
    """
    Provides personalized product recommendations based on customer profile and usage patterns.
    Args:
        customer_id: The customer's ID
        context: Additional context for recommendations (e.g., "gaming", "streaming", "business")
    """
    recommendations = {
        "74829": {  # Jane Doe - tech-savvy, interested in premium services
            "default": [
                {
                    "product_id": "bundle_pro_01",
                    "name": "Pro Fiber + TV Bundle",
                    "price": 159.99,
                    "savings": 30.00,
                    "reason": "Upgrade from basic internet, aligns with premium interest",
                    "features": ["940 Mbps", "300+ channels", "WiFi 6 router"]
                },
                {
                    "product_id": "mobile_premium_01",
                    "name": "Premium Mobile Plan",
                    "price": 80.00,
                    "savings": 15.00,
                    "reason": "Complement home internet with premium mobile service",
                    "features": ["Unlimited 5G", "Mobile hotspot", "Premium streaming"]
                }
            ],
            "gaming": [
                {
                    "product_id": "fiber_gamer_01",
                    "name": "Gamer Pro Package",
                    "price": 129.99,
                    "features": ["Low latency", "Static IP", "Premium router"]
                }
            ]
        },
        "99101": {  # John Smith - family user, values reliability
            "default": [
                {
                    "product_id": "family_bundle_01",
                    "name": "Family Premium Bundle",
                    "price": 199.99,
                    "savings": 45.00,
                    "reason": "Perfect for family entertainment and multiple devices",
                    "features": ["Gigabit internet", "Premium TV", "Parental controls"]
                }
            ]
        }
    }
    
    customer_recs = recommendations.get(customer_id, {"default": []})
    return json.dumps({
        "recommendations": customer_recs.get(context, customer_recs["default"])
    })

@tool
def get_service_status(customer_id: str) -> str:
    """
    Retrieves the current status of all services for a customer.
    """
    status_info = {
        "74829": {
            "internet": {
                "status": "active",
                "last_checked": "2025-08-27T10:00:00",
                "signal_strength": "excellent",
                "current_speed": "195 Mbps",
                "uptime": "99.9%",
                "recent_issues": []
            },
            "equipment": {
                "router": {
                    "status": "online",
                    "model": "VZ-Router-2000",
                    "last_restart": "2025-08-20T00:00:00"
                }
            }
        },
        "99101": {
            "internet": {
                "status": "active",
                "last_checked": "2025-08-27T10:00:00",
                "signal_strength": "good",
                "current_speed": "850 Mbps",
                "uptime": "99.8%",
                "recent_issues": [
                    {
                        "date": "2025-08-25",
                        "type": "brief_outage",
                        "resolved": True
                    }
                ]
            },
            "tv": {
                "status": "active",
                "signal_strength": "excellent",
                "recent_issues": []
            }
        }
    }
    
    return json.dumps(status_info.get(customer_id, {
        "error": "Customer not found"
    }))

@tool
def get_billing_summary(customer_id: str) -> str:
    """
    Retrieves billing information and payment history for a customer.
    """
    billing_info = {
        "74829": {
            "current_balance": 79.99,
            "due_date": "2025-09-15",
            "last_payment": {
                "amount": 79.99,
                "date": "2025-08-15",
                "method": "credit_card"
            },
            "auto_pay": True,
            "payment_history": [
                {"date": "2025-08-15", "amount": 79.99, "status": "paid"},
                {"date": "2025-07-15", "amount": 79.99, "status": "paid"},
                {"date": "2025-06-15", "amount": 79.99, "status": "paid"}
            ],
            "promotions_applied": ["autopay_discount"]
        }
    }
    
    return json.dumps(billing_info.get(customer_id, {
        "error": "Customer billing information not found"
    }))

@tool
def check_upgrade_eligibility(customer_id: str) -> str:
    """
    Checks customer's eligibility for service upgrades and special offers.
    """
    eligibility_info = {
        "74829": {
            "eligible_upgrades": [
                {
                    "type": "internet",
                    "name": "Pro Fiber Upgrade",
                    "details": "Eligible for discounted upgrade to Pro Fiber",
                    "special_pricing": 89.99,
                    "regular_price": 109.99,
                    "contract_required": False
                },
                {
                    "type": "bundle",
                    "name": "TV Add-on",
                    "details": "Add TV service at promotional rate",
                    "special_pricing": 49.99,
                    "regular_price": 69.99,
                    "duration_months": 12
                }
            ],
            "loyalty_rewards": [
                {
                    "type": "discount",
                    "description": "Loyalty discount available",
                    "amount": 10.00
                }
            ],
            "next_upgrade_date": "2025-09-01"
        }
    }
    
    return json.dumps(eligibility_info.get(customer_id, {
        "error": "Customer eligibility information not found",
        "eligible_upgrades": [],
        "loyalty_rewards": []
    }))

@tool
def get_support_history(customer_id: str) -> str:
    """
    Retrieves customer support interaction history.
    """
    support_history = {
        "74829": {
            "recent_interactions": [
                {
                    "date": "2025-07-10",
                    "type": "technical_support",
                    "issue": "Slow internet speeds",
                    "resolution": "Router reset resolved the issue",
                    "satisfaction_score": 5
                },
                {
                    "date": "2025-05-20",
                    "type": "sales_inquiry",
                    "topic": "TV package information",
                    "outcome": "Customer considering upgrade options",
                    "follow_up_scheduled": "2025-09-01"
                }
            ],
            "open_tickets": [],
            "preferred_contact_method": "email",
            "satisfaction_average": 4.8
        }
    }
    
    return json.dumps(support_history.get(customer_id, {
        "error": "Customer support history not found",
        "recent_interactions": [],
        "open_tickets": []
    }))

@tool
def calculate_bundle_savings(services: List[str], customer_id: Optional[str] = None) -> str:
    """
    Calculates potential savings from bundling services.
    Args:
        services: List of service IDs to bundle
        customer_id: Optional customer ID for personalized pricing
    """
    base_prices = {
        "internet_basic": 49.99,
        "internet_pro": 89.99,
        "tv_basic": 50.00,
        "tv_premium": 89.99,
        "mobile_unlimited": 75.00
    }
    
    bundle_discounts = {
        2: 0.10,  # 10% off for 2 services
        3: 0.15,  # 15% off for 3 services
        4: 0.20   # 20% off for 4 or more services
    }
    
    total_base_price = sum(base_prices.get(service, 0) for service in services)
    discount = bundle_discounts.get(len(services), 0)
    discounted_price = total_base_price * (1 - discount)
    
    return json.dumps({
        "original_price": total_base_price,
        "bundled_price": round(discounted_price, 2),
        "monthly_savings": round(total_base_price - discounted_price, 2),
        "annual_savings": round((total_base_price - discounted_price) * 12, 2),
        "discount_percentage": f"{discount * 100}%"
    })
