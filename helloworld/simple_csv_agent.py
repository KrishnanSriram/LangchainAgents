import pandas as pd
from langchain.agents import AgentType
from langchain.agents.initialize import initialize_agent
from langchain.tools import Tool
from langchain_ollama import ChatOllama
# from langchain_community.agent_toolkits.load_tools import load_tools
# from langchain_core.prompts import PromptTemplate

def get_model(name: str) -> ChatOllama:
  return ChatOllama(model=name)


def load_csv_into_df(file_name: str) -> pd.DataFrame:
  try:
    df = pd.read_csv(file_name=file_name)
    return df
  except Exception as e:
    return f"Error loading file: {str(e)}"


# Define a Tool to Query the CSV Data
def query_csv(query: str) -> str:
  """Answers questions based on data in a CSV file."""
  try:
    file_path = "./data.csv"
    df = load_csv_into_df(file_name=file_path)
    data_str = df.to_string(index=False)
    print("Data as STRING")
    print("===================")
    print(data_str)
    print("===================")
    llm = get_model(name="mistral")
    prompt = f"Given the following data:\n\n{data_str}\n\nAnswer this question:\n{query}"
    response = llm.invoke(prompt)
    return response
  except Exception as e:
    return f"Error processing query: {str(e)}"


def init_agents():
  tools = [Tool(
    name= "QueryCSV",
    func=query_csv,
    description="Query CSV file for all sales related information"
  )]
  agent = initialize_agent(tools=tools, llm=get_model("llama3.2"), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
  return agent


def main():
  agent = init_agents()
  question = "How many laptops were sold?"
  response = agent.invoke(question)
  print("Agent Response - ", response)


if __name__ == "__main__":
  main()