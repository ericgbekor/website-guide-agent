"""Agent module for the website navigation agent."""

import logging
import warnings
from google.adk import Agent
from google.genai import types
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .tools import (
    get_website_services,
    get_website_navigation
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# configure logging __name__
logger = logging.getLogger(__name__)

safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

# Safety settings for the agent
generate_content_config = types.GenerateContentConfig(
   safety_settings=safety_settings,
)


root_agent = Agent(
    model=configs.agent_settings.model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[
         get_website_services,
         get_website_navigation
    ],
    generate_content_config=generate_content_config,
)


