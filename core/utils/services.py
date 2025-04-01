import importlib, json, os
from core.utils.logger import logger
from core.utils.config import config


# Load services (without middleware for the main app)
def load_services(app):

    try:

        for service in config.get("SERVICES", []):
            try:
                module = importlib.import_module(f"{service}")
                app.include_router(module.router)
                logger.info(f"✅ Loaded services in {service}")
            except Exception as e:
                logger.error(f"❌ Failed to load services in '{service}': {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"❌ Error decoding JSON from configuration file: {str(e)}")
    except Exception as e:
        logger.error(
            f"❌ An unexpected error occurred while loading services: {str(e)}"
        )
