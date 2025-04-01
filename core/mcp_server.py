# server.py
from mcp.server.fastmcp import FastMCP
from core.utils.env import EnvConfig
from core.utils.logger import logger
from core.utils.tools import register_tools

# Initialize FastMCP
mcp = FastMCP(
    EnvConfig.SERVER_NAME,
    **{
        "host": EnvConfig.HOST,
        "port": EnvConfig.PORT,
        "debug": EnvConfig.DEBUG_MCP,
        "log_level": EnvConfig.LOG_LEVEL,
    },
)

logger.info("🔧 MCP Server settings: %s", mcp.settings)


# Call the function to register all tools
mcp = register_tools(mcp)


def run_fastmcp():
    logger.info("Starting FastMCP Server")
    mcp.run(transport="sse")
