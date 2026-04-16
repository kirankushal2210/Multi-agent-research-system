from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS

def search_duckduckgo(topic: str) -> str:
      """Useful for finding current information about a topic."""
      with DDGS() as ddgs:
                results = [r for r in ddgs.text(f"recruitment overview of {topic}", max_results=3)]
                if results:
                              return "\n".join([f"{r['title']}: {r['body']}" for r in results])
                      return "No results found."

def get_page_content(url: str) -> str:
      """Useful for reading a specific webpage."""
      try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                return soup.get_text()[:1500]
except Exception as e:
        return f"Error reading page: {str(e)}"
