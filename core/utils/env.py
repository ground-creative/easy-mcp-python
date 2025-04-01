import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class EnvConfig:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    SERVER_NAME = os.getenv("SERVER_NAME", "MCP Server")
    DEBUG_MCP = os.getenv("DEBUG", True)
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")

    @classmethod
    def get(self, key: str, default=None) -> str:
        """
        Retrieves the value of an environment variable.

        Args:
            key (str): The environment variable key.
            default (str, optional): Default value if key is not found. Defaults to None.

        Returns:
            str: The environment variable value or default if not found.
        """
        return os.getenv(key, default)
