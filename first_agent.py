from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.tools import tool
from langchain_ollama import OllamaLLM

@tool
def say_hello(name: str) -> str:
    """Says hello to the user."""
    return f"Hi {name}, nice to meet you!"

@tool
def calculate(expression: str) -> str:
    """Calculates the result of simple arithmetic expressions"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def main():
  agent = initialize_agent(
      tools=[say_hello, calculate],  
      llm=OllamaLLM(model="gemma3:12b"),
      agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
      verbose=False,
      handle_parsing_errors=True
  )

  # 🧪 Try it out
  print(agent.invoke("Say hello to Alice"))
  print(agent.invoke("What is 10 squared plus 5?"))

if __name__ == "__main__":
    main()