import json
from typing import List
from langchain.tools import tool
from langchain.tools import Tool



# Define the credit card data
BANK_CREDIT_CARDS = {
    "RewardsPlus": {
        "description": "Earn points on all purchases, ideal for everyday spending.",
        "rewards_structure": "1.5x points on all purchases",
        "annual_fee": 0,
        "benefits": ["Purchase protection", "Extended warranty"],
        "ideal_for": ["Everyday spending", "Simple rewards"],
    },
    "TravelElite": {
        "description": "Premium travel card with excellent travel rewards and benefits.",
        "rewards_structure": "2x miles on travel and dining, 1x on everything else",
        "annual_fee": 99,
        "benefits": ["Airport lounge access", "Travel insurance", "No foreign transaction fees"],
        "ideal_for": ["Frequent travelers", "Dining enthusiasts"],
    },
    "CashBackSaver": {
        "description": "Earn cash back on every purchase.",
        "rewards_structure": "2% cash back on two categories of your choice, 1% on everything else",
        "annual_fee": 0,
        "benefits": ["Cash back rewards", "Balance transfer options"],
        "ideal_for": ["Cash back focused users", "Managing expenses"],
    },
}

def recommend_credit_card_2(spending_habits: str = "online shopping",
    travel_frequency: str = "rarely",
    rewards_preference: str = "None"):
    # Scoring system to match user's preferences to card types
    scores = {
        "RewardsPlus": 0,
        "TravelElite": 0,
        "CashBackSaver": 0
    }

    # Match spending habits
    for card, data in BANK_CREDIT_CARDS.items():
        if spending_habits in data["ideal_for"]:
            scores[card] += 2

    # Match travel frequency
    if travel_frequency.lower() == "frequent":
        scores["TravelElite"] += 2
    elif travel_frequency.lower() == "occasional":
        scores["RewardsPlus"] += 1
        scores["TravelElite"] += 1
    else:  # "rare"
        scores["CashBackSaver"] += 1
        scores["RewardsPlus"] += 1

    # Match rewards preference
    if rewards_preference == "points":
        scores["RewardsPlus"] += 2
    elif rewards_preference == "miles":
        scores["TravelElite"] += 2
    elif rewards_preference == "cash":
        scores["CashBackSaver"] += 2

    # Determine best card
    best_card = max(scores, key=scores.get)
    return best_card

# Wrap the function as a tool using the @tool decorator
# @tool
def recommend_credit_card(
    spending_habits: str = "online shopping",
    travel_frequency: str = "rarely",
    preferred_rewards: str = "None"
) -> str:
    """
    Recommends a credit card from our bank based on your spending habits,
    travel frequency, and preferred rewards.

    Args:
        spending_habits (str): A description of your spending habits.
        travel_frequency (str): How frequently you travel.
        preferred_rewards (str): The type of rewards you prefer (e.g., points, miles, cash back).

    Returns:
        str: A recommendation for a credit card with a brief explanation.
    """
    print(f"Invoked recommend_credit_card with {spending_habits}, {travel_frequency}, {preferred_rewards} parameters!!")
    recommendations: List[str] = []
    for card_name, card_details in BANK_CREDIT_CARDS.items():
        suitability_score = 0

        # Simple keyword matching for spending habits
        for habit in spending_habits.lower().split():
            # Join the list of ideal_for items into a single string for keyword matching
            if habit in card_details["description"].lower() or habit in " ".join(card_details["ideal_for"]).lower():
                suitability_score += 1
        # Matching travel frequency
        if "travel" in travel_frequency.lower() and "travel" in " ".join(card_details["ideal_for"]).lower():
            suitability_score += 2
        elif "frequent" in travel_frequency.lower() and "frequent" in " ".join(card_details["ideal_for"]).lower():
            print("Frequent traveller")
            suitability_score += 2
        elif "rarely" in travel_frequency.lower() and "travel" not in " ".join(card_details["ideal_for"]).lower():
           suitability_score += 1

 
        # Matching preferred rewards
        if (preferred_rewards.lower() in card_details["description"].lower() or
            preferred_rewards.lower() in " ".join(card_details["ideal_for"]).lower() or
            preferred_rewards.lower() in card_details["rewards_structure"].lower()):
            suitability_score += 2
        elif "points" in preferred_rewards.lower() and "points" in card_details["rewards_structure"].lower():
            suitability_score += 1
        elif "miles" in preferred_rewards.lower() and "miles" in card_details["rewards_structure"].lower():
            suitability_score += 1
        elif "cash back" in preferred_rewards.lower() and "cash back" in card_details["rewards_structure"].lower():
            suitability_score += 1
 
        if suitability_score > 1:  # Adjust threshold as needed
            recommendations.append(
                (card_name, suitability_score, f"Card type - {card_name}, Score - {suitability_score}\n"
                f"Based on your preferences, the '{card_name}' card might be a good fit. "
                f"It offers {card_details['description']} with a rewards structure of '{card_details['rewards_structure']}'. "
                f"Key benefits include: {', '.join(card_details['benefits'])}. Annual fee: ${card_details['annual_fee']}.")
            )
    
        print(f"{card_name} and score {suitability_score}")
    if recommendations:
        final_score = 0
        choice = f""
        for recommendation in recommendations:
            (card, score, result) = recommendation
            print("Evaluating ", card, score, final_score)
            if score > final_score:
                final_score = score
                choice = result
        # return "\n".join(result)
        return choice
    else:
        return "Based on the information provided, we don't have a clear recommendation at this time. Please provide more details about your needs."

 
@tool
# Define tools (example: checking balance, making payments)
def check_balance(account_id):
    """Checks the balance of a bank account."""
    # Replace with actual banking API call
    balance = 1000 
    return f"The balance for account {account_id} is ${balance}"

 
@tool
def make_payment(account_id, recipient, amount):
    """Makes a payment from a bank account."""
    # Replace with actual banking API call
    return f"Payment of ${amount} to {recipient} from account {account_id} processed."


bank_tools = [
    Tool(
        name="Check Balance",
        func=check_balance,
        description="Useful for checking the balance of a bank account. Input: account ID.",
    ),
    Tool(
        name="Make Payment",
        func=make_payment,
        description="Useful for making a payment. Input: account ID, recipient, amount.",
    ),
    Tool(
        name="Choose CreditCard",
        func=recommend_credit_card_2,
        description="Recommends a credit card from our bank. Input: spending habits, travel frequency, preferred rewards",
    ),
]

# Example usage of the tool in a standalone script:
if __name__ == "__main__":
    # Define some example input parameters
    spending_habits = "I spend a lot on dining and everyday purchases."
    travel_frequency = "I travel frequently."
    preferred_rewards = "miles"
    # Get and print the credit card recommendation
    result = recommend_credit_card_2(spending_habits, travel_frequency, preferred_rewards)
    print("Recommendation:\n", result)