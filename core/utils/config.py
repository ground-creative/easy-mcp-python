# core/utils/config.py

import importlib.util
import os


class Config:
    def __init__(self, config_file_path=None):
        self._config = {}

        # Load the configuration file if it exists
        if config_file_path and os.path.exists(config_file_path):
            self.load_config(config_file_path)

    def load_config(self, config_file_path):
        """Load configuration from the specified file."""
        spec = importlib.util.spec_from_file_location("config_module", config_file_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        # Add all attributes from the module to the config dictionary
        for key in dir(config_module):
            if not key.startswith("__"):
                self._config[key] = getattr(config_module, key)

    def get(self, key, defaultValue=None):
        """Get a configuration value by key. Return defaultValue if the key does not exist."""
        return self._config.get(key, defaultValue)

    def set(self, key, value):
        """Set a configuration value by key."""
        self._config[key] = value

    def update(self, key, value):
        """Update a specific configuration value."""
        if key in self._config:
            self._config[key] = value
        else:
            raise KeyError(f"Configuration key '{key}' not found.")

    def all(self):
        """Return all configuration values."""
        return self._config


# Create an instance of the Config class
config_file_path = os.path.join(os.path.dirname(__file__), "../../app/config/app.py")
config = Config(config_file_path)
