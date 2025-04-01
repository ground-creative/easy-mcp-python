from core.utils.logger import logger


class GlobalState:
    def __init__(self):
        self._state = {}

    def set(self, name: str, value: str, override: bool = False):
        """Dynamically set a variable in the state.

        Args:
        - name (str): The name of the variable.
        - value (str): The value to be set.
        - override (bool): If False, an error is thrown if the key already exists.
        """
        if not override and name in self._state:
            logger.error(f"Key '{name}' already exists in state and override is False.")
            return

        self._state[name] = value

    def get(self, name: str, default=None):
        """Dynamically get a variable from the state, returning a default value if not found."""
        return self._state.get(name, default)

    def get_all(self):
        """Return all stored state variables."""
        return self._state


global_state = GlobalState()
