import os
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import pandas as pd

# 2. Define the Tools (Calculator and Greeter)
def calculate(expression: str) -> str:
    """Calculates the result of a simple arithmetic expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def greet(name: str) -> str:
    """Greets the person with the given name."""
    return f"Hello, {name}! How can I help you today?"


def csv_data_to_file(file_name="laptop_sales.csv"):
  csv_data = {
    'Region': ['North', 'North', 'South', 'South', 'East', 'West', 'West'],
    'Product': ['Laptop A', 'Laptop B', 'Laptop A', 'Laptop C', 'Laptop B', 'Laptop C', 'Laptop A'],
    'Sales': [150, 200, 180, 220, 160, 210, 190]
  }
  df = pd.DataFrame(csv_data)
  csv_file_path = file_name
  df.to_csv(csv_file_path, index=False)


def csv_agent(csv_file_path="laptop_sales.csv"):  
  return create_csv_agent(
    llm=Ollama(model="llama3.2"),
    path=csv_file_path,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # Or try AgentType.OPENAI_FUNCTIONS if Llama3 supports function calling well,
    allow_dangerous_code=True
  )


def create_tools():
  csv_file = "laptop_sales.csv"
  csvagent = csv_agent()
  tools = [
    Tool(
        name="Calculator",
        func=calculate,
        description="Useful for performing basic arithmetic calculations.",
    ),
    Tool(
        name="Greeter",
        func=greet,
        description="Useful for providing a personalized greeting.",
    ),
    Tool(
        name="Laptop Sales Data",
        func=csvagent.invoke,
        description=f"Useful for answering questions about laptop sales data in the file '{csv_file}'. Input should be a question about the sales data.",
    ),
  ]

  return tools


def create_agent():
  csv_file_path="laptop_sales.csv"
  all_tools = create_tools()

  regular_agent = initialize_agent(
      llm=Ollama(model="llama3.2"),
      tools=all_tools,
      agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
      verbose=True,
  )
  return regular_agent

def main_csv_agent():
  csv_data_to_file()
  laptop_csv_agent = csv_agent()
  result_csv = laptop_csv_agent.invoke("What were the total sales of Laptop A across all regions?")
  print(f"Regular Agent Response (CSV Data): {result_csv}")

  print("\n--- Running the regular agent with another CSV data query ---")
  result_csv_region = laptop_csv_agent.invoke("What was the average sales in the North region?")
  print(f"Regular Agent Response (CSV Data - Region): {result_csv_region}")

  print("\n--- Running the CSV agent directly ---")
  result_csv_direct = laptop_csv_agent.invoke("How many unique products are there?")
  print(f"CSV Agent Direct Response: {result_csv_direct}")

def main():
  csv_data_to_file()
  regular_agent = create_agent()

  print("--- Running the regular agent with a calculation query ---")
  result_calc = regular_agent.invoke("What is 10 squared plus 5?")
  print(f"Regular Agent Response (Calculation): {result_calc}")

  print("\n--- Running the regular agent with a greeting query ---")
  result_greet = regular_agent.invoke("Say hello to Bob.")
  print(f"Regular Agent Response (Greeting): {result_greet}")

  print("\n--- Running the regular agent with a CSV data query ---")
  result_csv = regular_agent.invoke("What were the total sales of Laptop A across all regions?")
  print(f"Regular Agent Response (CSV Data): {result_csv}")

  # print("\n--- Running the regular agent with another CSV data query ---")
  # result_csv_region = regular_agent.run("What was the average sales in the North region?")
  # print(f"Regular Agent Response (CSV Data - Region): {result_csv_region}")

  # print("\n--- Running the CSV agent directly ---")
  # result_csv_direct = csv_agent.run("How many unique products are there?")
  # print(f"CSV Agent Direct Response: {result_csv_direct}")


if __name__ == "__main__":
   main()
  #  main_csv_agent()