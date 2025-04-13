from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_ollama import ChatOllama
from langchain.agents import load_tools

# Define model to use
def get_llm(name="llama3.2") -> ChatOllama:
  return ChatOllama(name=name)


# Define the Tools
def calculate(expression: str) -> str:
    # Calculates the result of a simple arithmetic expression.
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"
    

def greet(name: str) -> str:
    # Greets the person with the given name
    return f"Hello, {name}! How can I help you today?"


def main():
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
  ]

  llm = Ollama(model="llama3.2")
  # Initialize the Agent
  agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Set to True to see the agent's thought process
  )

  # Run the Agent with Different Queries
  print("--- Running the agent with a calculation query ---")
  result_calc = agent.invoke("What is 5 plus 7 multiplied by 3?")
  print(f"Agent Response: {result_calc}")

  print("\n--- Running the agent with a greeting query ---")
  result_greet = agent.invoke("Say hello to Alice.")
  print(f"Agent Response: {result_greet}")

  # print("\n--- Running the agent with a slightly ambiguous query ---")
  # result_ambiguous = agent.invoke("What is the answer to life, the universe, and everything?")
  # print(f"Agent Response: {result_ambiguous}")


if __name__ == "__main__":
   main()
    
