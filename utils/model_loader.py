import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

  # updated import
from config.config_loader import load_config

class ModelLoader:
    def __init__(self):
        """Initialize the model loader and load environment variables."""
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        self.model_name = self.config['llm']['model_name']
        self.temperature = self.config['llm'].get('temperature', 0.5)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def _validate_env(self):
        """Validate necessary environment variables."""
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_model(self):
        """Load the OpenAI model with specified parameters."""
        return ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.openai_api_key
        )
