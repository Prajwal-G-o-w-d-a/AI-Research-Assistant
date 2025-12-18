from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool  # ← CHANGED THIS
from datetime import datetime

# Create save tool using @tool decorator
@tool
def save_text_to_file(data: str, filename: str = "research_output.txt") -> str:
    """Saves structured research data to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Create save_tool from the decorated function
save_tool = save_text_to_file

# Create search tool using @tool decorator
@tool
def search(query: str) -> str:
    """Search the web for information"""
    search_engine = DuckDuckGoSearchRun()
    return search_engine.run(query)

search_tool = search

# Create wiki tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)