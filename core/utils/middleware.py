import importlib, json
from core.utils.logger import logger
from core.utils.config import config
from starlette.middleware.base import BaseHTTPMiddleware


def load_middleware(app, type="mcp"):

    middlewares = []
    configuration = config.get("MIDDLEWARE", {})

    if len(configuration) == 0:
        return middlewares

    middleware_configs = configuration.get(type, [])

    if len(middleware_configs) == 0:
        return middlewares

    try:
        # Sort middlewares by priority (lower value = higher priority)
        middleware_configs.sort(key=lambda x: x.get("priority", 0), reverse=True)
        for middleware_config in middleware_configs:
            middleware_path = middleware_config.get("middleware")
            args = middleware_config.get("args", {})  # Extract optional arguments

            try:
                logger.debug(f"Attempting to load middleware: {middleware_path}")
                module_name, class_name = middleware_path.rsplit(".", 1)

                # Import module dynamically
                module = importlib.import_module(middleware_path)
                middleware_class = getattr(module, class_name)

                # Ensure it’s a subclass of BaseHTTPMiddleware
                if not issubclass(middleware_class, BaseHTTPMiddleware):
                    raise TypeError(
                        f"{class_name} is not a subclass of BaseHTTPMiddleware."
                    )

                # Instantiate middleware (ALWAYS pass `app`, optionally pass `args`)
                middleware_instance = app.add_middleware(middleware_class, **args)
                middlewares.append(middleware_instance)
                logger.info(
                    f"✅ Successfully loaded MCP middleware: {middleware_class.__name__}"
                )

            except ModuleNotFoundError as e:
                logger.error(f"❌ Module not found: {module_name}. Error: {e}")
            except AttributeError as e:
                logger.error(
                    f"❌ Class '{class_name}' not found in module '{module_name}'. Error: {e}"
                )
            except Exception as e:
                logger.error(f"❌ Error loading middleware '{middleware_path}': {e}")

    except json.JSONDecodeError as e:
        logger.error(f"❌ Error parsing JSON config: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error reading config file: {e}")

    return middlewares
