from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import tool
from langchain_ollama.llms import OllamaLLM
import re

credit_cards = {
    "Travel Rewards Card": {
        "features": "Excellent for earning points on travel expenses.",
        "suitable_for": "Frequent travelers",
    },
    "Cashback Rewards Card": {
        "features": "Earns a percentage of cashback on all purchases.",
        "suitable_for": "Everyday spending",
    },
    "Low Interest Card": {
        "features": "Offers a low APR for balance transfers and purchases.",
        "suitable_for": "Carrying a balance",
    },
    "Student Card": {
        "features": "Designed for students with limited credit history.",
        "suitable_for": "Students",
    },
    "Business Card":{
        "features": "Designed for business owners, with extra perks.",
        "suitable_for": "Business Owners",
    }
}

llm = OllamaLLM(model="gemma3:12b")

# Define custom tools for credit card and investment banking advice
@tool
def credit_card_advice(query: str) -> str:
    """Provides credit card advice based on the user's query and needs, using LLM reasoning."""

    card_descriptions = "\n".join(
        [f"{name}: {card['features']}. Suitable for: {card['suitable_for']}" for name, card in credit_cards.items()]
    )

    prompt = f"""
    Given the following credit card descriptions:
    {card_descriptions}

    And the user's query:
    {query}

    Which credit card is the most suitable for the user? Explain your reasoning.
    """

    response = llm(prompt=prompt)
    return response

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