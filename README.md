## AI Research Assistant (LangChain + Gemini)

This project is a simple command-line **AI research assistant** built with **LangChain** and **Google Gemini**. It can:

- **Search the web** using DuckDuckGo  
- **Query Wikipedia** for focused background information  
- **Aggregate findings** into a structured research summary  
- **Optionally save** the final research output to a local text file

The core logic lives in `main.py`, and the tools (web search, Wikipedia, save-to-file) are defined in `tools.py`.

---

### How It Works

- `main.py`:
  - Loads environment variables with `python-dotenv`.
  - Defines a `ResearchResponse` Pydantic model to structure the final answer.
  - Creates a `ChatGoogleGenerativeAI` LLM (Gemini) and binds tools from `tools.py`.
  - Asks you: **"What can I help you research?"** in the terminal.
  - Iteratively:
    - Lets Gemini decide which tools to call.
    - Executes those tools (search, wiki, save).
    - Feeds tool results back into the conversation.
  - Finally parses the LLM output into a `ResearchResponse` and prints it.

- `tools.py`:
  - `search_tool`: Uses DuckDuckGo (`DuckDuckGoSearchRun`) to search the web.
  - `wiki_tool`: Uses `WikipediaQueryRun` to fetch content from Wikipedia.
  - `save_tool` (`save_text_to_file`): Saves structured research output into a timestamped text file (default: `research_output.txt`).

---

### Requirements

All Python dependencies are listed in `requirements.txt`, including:

- `langchain`, `langchain-community`
- `langchain-google-genai` (implicitly used via `ChatGoogleGenerativeAI`)
- `wikipedia`
- `duckduckgo-search`
- `python-dotenv`
- `pydantic`

You will also need a **Google Generative AI (Gemini) API key**.

---

### Setup

1. **Clone the repository**

```bash
git clone <YOUR_REPO_URL>.git
cd <YOUR_REPO_NAME>
```

2. **Create and activate a virtual environment** (recommended)

```bash
python -m venv .venv
.\.venv\Scripts\activate  # on Windows
# source .venv/bin/activate  # on macOS / Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root with your Gemini API key:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

### Usage

Run the assistant from the project root:

```bash
python main.py
```

You will be prompted:

```text
What can i help you research?
```

Type any research topic or question (e.g. *"Impacts of quantum computing on cryptography"*).  
The assistant will:

- Call web search and/or Wikipedia tools as needed.
- Optionally use the save tool to persist the research output.
- Print a **structured research result** matching the `ResearchResponse` schema:
  - `topic`
  - `summary`
  - `sources`
  - `tools_used`

If `save_tool` is called, a file like `research_output.txt` will be created/updated with timestamped entries.

---

### Project Structure

```text
.
├─ main.py        # CLI entrypoint, LLM + tool orchestration, parsing & printing final result
├─ tools.py       # Definitions of search, Wikipedia, and save-to-file tools
└─ requirements.txt
```

---

### Pushing to GitHub

After you’ve reviewed/edited this `README.md`, you can push everything to GitHub:

```bash
git init             # if this is a new repo
git add .
git commit -m "Initial commit: AI research assistant"
git remote add origin <YOUR_REPO_URL>
git push -u origin main  # or 'master', depending on your default branch
```

---

### Future Improvements (Ideas)

- Add a simple **CLI menu** (e.g. `argparse` or `typer`) for different modes (quick summary vs deep dive).
- Support **multiple output formats** (Markdown, PDF, HTML).
- Cache web/Wikipedia results to reduce repeated calls.
- Add tests for tools and parsing logic.


