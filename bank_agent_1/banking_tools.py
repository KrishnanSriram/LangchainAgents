from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import tool
import re


# Define custom tools for credit card and investment banking advice
@tool
def credit_card_advice(query: str) -> str:
    """Provides credit card advice based on the user's query."""
    search = DuckDuckGoSearchRun()
    search_results = search.run(f"credit card {query}")
    advice = f"Here's some credit card advice based on your query:\n{search_results}"
    return advice

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