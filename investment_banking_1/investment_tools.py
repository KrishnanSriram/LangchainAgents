from langchain_ollama import OllamaLLM
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool
import random

@tool
def multiply_numbers(input: str) -> str:
  """Multiplies two numbers provided in the input string, e.g., '3 and 4'."""
  try:
    a, b = [int(x.strip()) for x in input.split("and")]
    return str(a * b)
  except:
      return "Please provide two integers like '3 and 4'."
  

# Tool for market research
@tool
def get_recommended_shares(input: str) -> str:
    """Returns a list of recommended shares to buy based on mock logic."""
    return ["AAPL", "MSFT", "NVDA"]

# Tool for executing trades
@tool
def buy_shares(input: str) -> str:
    """Buys the given shares and returns a confirmation with cost."""
    shares = input.split(",")
    result = []
    for s in shares:
        cost = round(random.uniform(100, 500), 2)
        result.append(f"Bought {s.strip()} at ${cost}")
    return "\n".join(result)

# Tool for notification
@tool
def notify_user(input: str) -> str:
    """Sends a notification to the user about the trade."""
    return f"User notified with message:\n{input}"