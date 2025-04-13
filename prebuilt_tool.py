# from langchain_community.llms import ollama
from langchain_community.tools import DuckDuckGoSearchResults
import datetime

class Result:
  def __init__(self, snippet:str, title: str, link: str):
    self.snippet = snippet
    self.title = title
    self.link = link

  def __repr__(self):
    return f"Result(Snippet='{self.snippet}'\nTitle='{self.title}'\nLink='{self.link}'\n)"


def main():
  search_tool = DuckDuckGoSearchResults(max=1, output_format="list")

  query = "Cities in Italy"
  results = search_tool.invoke(query)

  all_results = []
  if results:
    for result in results:
      all_results.append(Result(result["snippet"], result["title"], result["link"]))
  else:
    print("Search operation FAILED. Try again")
    return
  print(all_results)


if __name__ == "__main__":
  main()

