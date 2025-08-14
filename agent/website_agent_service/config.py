"""Configuration module for the website navigation agent."""

import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentModel(BaseModel):
    """Agent model settings."""

    name: str = Field(default="web_agent_service_agent")
    model: str = Field(default="gemini-2.5-flash")


class Config(BaseSettings):
    """Configuration settings for the website navigation agent."""

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env"
        ),
        case_sensitive=True,
    )
    agent_settings: AgentModel = Field(default=AgentModel())
    app_name: str = "web_agent_service_app"
    GOOGLE_CLOUD_PROJECT: str = Field(default="my_project")
    GOOGLE_CLOUD_LOCATION: str = Field(default="europe-west2")
    GOOGLE_GENAI_USE_VERTEXAI: str = Field(default="1")
    GOOGLE_API_KEY: str | None = Field(default="")
    WEBSITE_API_URL: str | None = Field(default="")
    
    @property
    def CLOUD_PROJECT(self):
        return self.GOOGLE_CLOUD_PROJECT
    
    @property 
    def CLOUD_LOCATION(self):
        return self.GOOGLE_CLOUD_LOCATION
