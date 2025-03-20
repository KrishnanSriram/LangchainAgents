from langchain_community.llms import ollama
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_model(name: str) -> ollama.Ollama:
  return ChatOllama(model="mistral")

def get_prompt_template():
  return PromptTemplate.from_template("Tell me on joke on {subject}")


def main():
  model = get_model("mistral")
  chain = get_prompt_template() | model | StrOutputParser()
  response = chain.invoke({"subject": "birds"})
  print(response)


if __name__ == "__main__":
  main()