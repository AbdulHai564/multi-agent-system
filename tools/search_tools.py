from tavily import TavilyClient
from config import *

client=TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query,depth="advanced",max_results=5):
    results=client.search(query=query,depth=depth,max_results=max_results)

    return results["results"]


def extract_pages(url,depth="advanced"):

    result=client.extract(urls=[url],extract_depth=depth)

    if result["results"]:
        return result["results"][0]["raw_content"]
    else:
        return ""