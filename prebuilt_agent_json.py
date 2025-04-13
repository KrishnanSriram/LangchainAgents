# from langchain.agents.agent_toolkits import JsonToolkit
from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.agent_toolkits import JsonToolkit
from langchain_core.tools import BaseTool
from langchain_community.tools.json.tool import JsonSpec
from langchain_ollama import ChatOllama
import json

def load_json_from(file_name: str) -> str:
  try:
      with open(file_name, "r") as json_file:
          data = json.load(json_file)
  except FileNotFoundError:
      print("ERROR: Can you please check path to file")
      exit()
  except json.JSONDecodeError:
      print(
          "ERROR: Invalid JSON format. Please check to see if this is a JSON file and is formatted right"
      )
      exit()
  return data


def json_spec_for_data(data: str, max_length=7000) -> JsonSpec:
  return JsonSpec(dict_=data, max_value_length=max_length)


def get_json_toolkit(spec: JsonSpec):
  return JsonToolkit(spec=spec)


def get_llm(model_name: str = "gemma3:12b") -> ChatOllama:
  return ChatOllama(model=model_name)


def main(file_name: str):
  json_content = load_json_from(file_name=file_name)
  json_spec = json_spec_for_data(data=json_content)
  json_toolkit = get_json_toolkit(spec=json_spec)
  tools = json_toolkit.get_tools()
  ollama_llm = get_llm(model_name="gemma3:12b")
  agen_executor = create_json_agent(
      llm=ollama_llm, toolkit=json_toolkit, verbose=False
  )
  queries = [{"input": "I purchase a lot of amenety items and will enjoy some rewards back. What's the card I should choose?"},
             {"input": "I do a lot of travel and buy stuff i international airports. What's the card I should choose?"},
             {"input": "I prefer doing a purchase on discounts and enjoy cashback, rewards etc. What's the card I should choose?"},
             {"input": "Can you tell me more about RewardsPlus?"}
             ]
  print("EXECUTE QUERIES")
  print("===============")
  for query in queries:
    result = agen_executor.invoke(
        query
    )
    print(result)
    print("----------------")

  print("=================")


if __name__ == "__main__":
  main("./data/card_details.json")
