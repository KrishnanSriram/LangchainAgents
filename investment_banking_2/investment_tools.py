from langchain_ollama import OllamaLLM
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool
import random
import psycopg2
import os

  

# Tool for market research
@tool
def get_recommended_shares(input: str) -> str:
    """Returns a list of recommended shares to buy based on mock logic."""
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, threshold_price, quantity FROM watchlist")
    rows = cursor.fetchall()
    conn.close()

    recommendations = []
    for symbol, threshold, quantity in rows:
        try:
            recommendations.append(f"{symbol}:{quantity}")
        except:
            continue

    return ", ".join(recommendations) if recommendations else "No shares in DB. Check your DB or connection to DB."

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