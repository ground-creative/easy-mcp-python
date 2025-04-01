import json
import importlib
from core.utils.logger import logger
from core.utils.config import config


def load_hooks(server_name, type="PRESTART_HOOKS"):
    """Load hooks from the JSON configuration file."""
    hooks = config.get(type, [])

    if len(hooks) == 0:
        return []

    return hooks.get(server_name, [])


def execute_hooks(hooks, server_name):
    """Execute the specified hooks."""
    for hook_path in hooks:
        try:
            # Dynamically import the module and function
            module_path, function_name = hook_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            hook_function = getattr(module, function_name)

            # Call the hook function with the server name
            result = hook_function(server_name)
            if result:
                logger.warning(
                    f"Hook '{hook_path}' for server '{server_name}' returned: {result}"
                )  # Log the result if any
        except Exception as e:
            logger.error(
                f"Error executing hook '{hook_path}' for server '{server_name}': {str(e)}"
            )


def pre_start_hook(server_name):
    """Hook to execute before starting the server."""
    hooks = load_hooks(
        server_name, "PRESTART_HOOKS"
    )  # Load hooks for the specified server

    if len(hooks) > 0:
        logger.debug(f"Executing pre-start hooks for {server_name} server...")

        execute_hooks(hooks, server_name)  # Execute the loaded hooks
    logger.info(f"Pre-start checks for {server_name} completed.")
