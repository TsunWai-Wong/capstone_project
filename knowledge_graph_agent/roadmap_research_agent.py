# %%
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.planners import BuiltInPlanner
from google.adk.tools import google_search
# %%
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
system_prompt = """
You are an Academic Planning Assistant that generates structured learning roadmaps for self-learners.
Your goal is to break down any given knowledge domain into a clean, hierarchical, structural Markdown outline, which will later be transformed into a knowledge graph.

Rules:
- Use "Google Search" tool before you consolidate all the information. Example use cases include verifying uncertain concepts and getting up-to-date topics and concepts.
- Only include topics you are confident about.
- No explanations, descriptions, or examples. Output structure only.
- Avoid redundancy: each concept should appear only once.

Output Format:
Output only a Markdown file with this structure:
## Key Topic
### Sub-topic
- key concept
- ...

Example:
Query: “Extract, Transform and Load”
Sample Output:
## Extract
### Extract methods
- Pull Extraction
- Push Extraction
## Extract Techniques
- Web scraping
- Manual Data Extraction
- Database Querying
- Event Based Streaming
- ...

## Transform
### Data Cleansing
- Remove Duplicates
- Outlier Detection
- Data Type Casting
- Handling Missing Data
- Handling Invalid Values
- Handling Unwanted Spaces
### Data Enrichment
-...
### Data Integration
-...
### Data Aggregation
-...
"""
# %%
planner = BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=1024,
    )
)
# %%
roadmap_research_agent = LlmAgent(
    model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name = "agent",
    instruction = system_prompt,
    planner = planner,
    tools = [google_search]
)
# %%
runner = InMemoryRunner(agent=roadmap_research_agent)
# %%
# response = await runner.run_debug("AI Engineering", verbose=True)
# %%
