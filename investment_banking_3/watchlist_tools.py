from typing import Optional
from pydantic import BaseModel
import psycopg2
from langchain.tools import tool
import os

class WatchEntry(BaseModel):
    symbol: str
    threshold_price: float
    quantity: int

def db_connection():
  conn = psycopg2.connect(
      host=os.getenv("HOST"),
      database=os.getenv("DATABASE"),
      user=os.getenv("DB_USER"),
      password=os.getenv("PASSWORD")
    )
  return conn

@tool
def add_stock(entry: str) -> str:
    """Adds a stock to the watchlist: input must be 'SYMBOL:PRICE:QTY'."""
    try:
        symbol, price, qty = entry.split(":")
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO watchlist (symbol, threshold_price, quantity) VALUES (%s, %s, %s) ON CONFLICT (symbol) DO NOTHING",
                       (symbol, float(price), int(qty)))
        conn.commit()
        conn.close()
        return f"Added {symbol}"
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def update_stock(entry: str) -> str:
    """Updates threshold/qty for a stock: 'SYMBOL:PRICE:QTY'."""
    try:
        symbol, price, qty = entry.split(":")
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE watchlist SET threshold_price=%s, quantity=%s WHERE symbol=%s",
                       (float(price), int(qty), symbol))
        conn.commit()
        conn.close()
        return f"Updated {symbol}"
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def delete_stock(symbol: str) -> str:
    """Deletes a stock from the watchlist."""
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watchlist WHERE symbol=%s", (symbol,))
        conn.commit()
        conn.close()
        return f"Deleted {symbol}"
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def get_all_stocks():
    """Get list of all stocks from watchlist"""
    print("Get all scrips....")
    conn = db_connection()
    print("DB connection established")
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, threshold_price, quantity FROM watchlist")
    results = cursor.fetchall()
    print("Got response from DB tables....")
    conn.close()
    print("Connection closed...")
    return [{"symbol": r[0], "threshold_price": r[1], "quantity": r[2]} for r in results]