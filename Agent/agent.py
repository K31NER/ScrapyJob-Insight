from Agent.model import *
from agno.agent import Agent
from Agent.prompt import SYSTEM_PROMPT
from Agent.schema import JobsProcces, JobEntry

redact_agent = Agent(
    model=ollama_model,
    instructions=SYSTEM_PROMPT,
    output_schema=JobsProcces,
    input_schema=JobEntry,
    debug_mode=False
)