from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    convert_system_message_to_human=True
)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Bind tools to the LLM
tools = [search_tool, wiki_tool, save_tool]
llm_with_tools = llm.bind_tools(tools)

query = input("What can i help you research? ")

# Create messages
messages = [
    SystemMessage(content=f"""
    You are a research assistant that will help generate a research paper.
    Answer the user query and use necessary tools.
    
    When you're done researching, provide your final answer in this exact format:
    {parser.get_format_instructions()}
    """),
    HumanMessage(content=query)
]

# Invoke the LLM with tools
response = llm_with_tools.invoke(messages)

# Handle tool calls if any
while response.tool_calls:
    print(f"\nUsing tools: {[tc['name'] for tc in response.tool_calls]}")
    
    # Execute each tool call
    for tool_call in response.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        
        # Find and execute the tool
        tool_to_use = next((t for t in tools if t.name == tool_name), None)
        if tool_to_use:
            result = tool_to_use.invoke(tool_args)
            print(f"Tool {tool_name} result: {result[:100]}...")
            
            # Add tool result to messages
            messages.append(response)
            from langchain_core.messages import ToolMessage
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call['id']))
    
    # Get next response
    response = llm_with_tools.invoke(messages)

# Parse final response
try:
    final_output = response.content
    structured_response = parser.parse(final_output)
    print("\n" + "="*50)
    print("FINAL RESEARCH OUTPUT:")
    print("="*50)
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e)
    print("Raw Response:", response.content)