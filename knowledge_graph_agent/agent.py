# %%
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool
from roadmap_research_agent import roadmap_research_agent
# from tools import write_to_file
# %%
# load the variables (incl. API keys) from .env to the environemnt variables
import os
from dotenv import load_dotenv
load_dotenv()
# %%
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# %%
def write_to_file(filename: str, content: str) -> dict:
    """
    Writes the provided content to a specified file on the local disk.

    Args:
        filename: The full name and path of the file to create or overwrite.
        content: The text content to write into the file.

    Returns:
        A dictionary with a 'status' key and a 'message' detailing the outcome.
    """
    try:
        # Check if the directory exists (optional, but good practice)
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
        with open(filename, 'w') as f:
            f.write(content)
        
        return {
            "status": "success",
            "message": f"Successfully wrote {len(content)} characters to file: {filename}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write to file: {filename}. Error: {str(e)}"
        }
# %%
system_prompt = """
You are an academic planning assistant that firstly create a hierarchical learning roadmap, and then turn it into a set of Obsidian-compatible markdown notes forming a knowledge graph.
When you receive the keyword from the user, you can get the roadmap by using the agent tool roadmap_research_agent by inputing the name of knowledge to it.
You will receive a roadmap of learning like this:
## Topic
### Sub-topic
- Concept
Your job is to convert this structure into an Obsidian vault. So you have to output by writing the files in the current directory. It should follow this structure.
Rules:
1. Every Topic, Sub-topic, and Concept becomes its own markdown file.
2. The filename must exactly match the name of the node, except you have to skip all these special characters: :/\?*"<>\| The .md extension must be included.
3. Inside each file, include the Obsidian links [[Linked Note]] to its related nodes. A link is defined as the followings:
- Sub-topics link to their parent Topic
- Concepts link to their parent Sub-topic
- Concepts under the same sub-topic should link to each other (to form a cluster in graph view)
- No other links are allowed. No extra or invented relationships.
4. For every Topic, Sub-topic, and Concept, you must call the tool: write_to_file(filename, content) like this: 
- filename must be the sanitized node name + .md
- content must contain a top-level heading with the file's name and the required links in Obsidian format
5. Your output should be only tool calls, one per file. Do not output markdown previews, explanations, descriptions, or any commentary.
6. Do not create relationships that are not explicitly implied by the roadmap hierarchy.
7. After all tool calls are complete, output a single completion message, e.g., “All notes have been created.”
"""
# %%
knowledge_graph_agent = LlmAgent(
    model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name = "agent",
    instruction = system_prompt,
    tools = [write_to_file, AgentTool(agent = roadmap_research_agent)]
)
# %%
root_agent = knowledge_graph_agent