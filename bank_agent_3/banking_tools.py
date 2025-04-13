from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import tool
import re

credit_cards = {
    "Travel Rewards Card": {
        "features": {"travel_rewards": 5, "cashback": 2, "apr": 3, "fees": 1},
        "suitable_for": "Frequent travelers",
    },
    "Cashback Rewards Card": {
        "features": {"travel_rewards": 1, "cashback": 5, "apr": 4, "fees": 2},
        "suitable_for": "Everyday spending",
    },
    "Low Interest Card": {
        "features": {"travel_rewards": 1, "cashback": 2, "apr": 5, "fees": 3},
        "suitable_for": "Carrying a balance",
    },
    "Student Card": {
        "features": {"travel_rewards": 2, "cashback": 3, "apr": 4, "fees": 4},
        "suitable_for": "Students",
    },
    "Business Card":{
        "features": {"travel_rewards": 3, "cashback": 4, "apr": 2, "fees": 5},
        "suitable_for": "Business Owners",
    }
}

feature_weights = {
    "travel": {"travel_rewards": 5, "cashback": 1, "apr": 2, "fees": 2},
    "cashback": {"travel_rewards": 1, "cashback": 5, "apr": 2, "fees": 1},
    "low interest": {"travel_rewards": 1, "cashback": 1, "apr": 5, "fees": 3},
    "student": {"travel_rewards": 2, "cashback": 3, "apr": 4, "fees": 4},
    "business": {"travel_rewards": 3, "cashback": 4, "apr": 2, "fees": 5}
}

# Define custom tools for credit card and investment banking advice
@tool
def credit_card_advice(query: str) -> str:
    """Provides credit card advice based on the user's query and needs using ranking/scoring."""
    query_lower = query.lower()
    user_features = {}

    if "travel" in query_lower:
        user_features = feature_weights["travel"]
    elif "cashback" in query_lower:
        user_features = feature_weights["cashback"]
    elif "low interest" in query_lower:
        user_features = feature_weights["low interest"]
    elif "student" in query_lower:
        user_features = feature_weights["student"]
    elif "business" in query_lower:
        user_features = feature_weights["business"]
    else:
        user_features = feature_weights["cashback"] #default

    card_scores = {}
    for card_name, card_data in credit_cards.items():
        score = 0
        for feature, weight in user_features.items():
            score += card_data["features"][feature] * weight
        card_scores[card_name] = score

    recommended_card = max(card_scores, key=card_scores.get)
    return f"Based on your needs, the {recommended_card} is recommended."

@tool
def investment_banking_advice(query: str) -> str:
    """Provides investment banking advice based on the user's query."""
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"investment banking {query}")
    advice = f"Here's some investment banking advice based on your query:\n{search_results}"
    return advice

@tool
def financial_calculator(expression: str) -> str:
    """Useful for performing mathematical calculations related to finance."""
    try:
        if re.search(r"[a-zA-Z]", expression):
            return "Invalid expression. Please only use numbers and operators."
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"