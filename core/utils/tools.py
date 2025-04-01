import importlib, os
from core.utils.logger import logger
from core.utils.env import EnvConfig


# Dynamically discover and register tools
def register_tools(mcp):
    tools_directory = os.path.join(
        os.path.dirname(__file__), "..", "..", "app", "tools"
    )
    for filename in os.listdir(tools_directory):

        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"app.tools.{filename[:-3]}"  # Remove '.py' extension
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if the attribute is a callable function and not a class
                    if (
                        callable(attr)
                        and hasattr(attr, "__name__")
                        and "tool" in attr.__name__.lower()
                        and not isinstance(attr, type)  # Ensure it's not a class
                    ):
                        mcp.tool()(attr)  # Register the tool dynamically
                        logger.info(f"🛠️  Registered tool: {attr.__name__}")

            except Exception as e:
                logger.error(
                    f"❌ Failed to register tool from {filename}: {e}",
                    exc_info=EnvConfig.DEBUG_MCP,
                )

    return mcp
