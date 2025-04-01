# Easy MCP Python

A simple python mvc framework to work with mcp servers.<br>
The framework uses a fastapi application to create services.

## Installation

1. Clone the repository

```
git clone https://github.com/ground-creative/easy-mcp-python.git
```

2. Change environment variables in env.sample file and rename it to .env

3. Create venv environment

```
python3 -m venv venv
source venv/bin/activate
```

4. Install requirements

```
pip install -r requirements.txt
```

## Run the server

To run the server you can use one of the following commands:

```
# Run via fastapi wrapper
python3 run.py -s fastapi

# Run the mcp server directly
python3 run.py -s fastmcp
```

## Adding Tools

Create tools in folder app/tools. Use `{function_name}_tool` name convention like this example:

```
# app/tools/add.py

from utils.application.logger import logger # Use to add logging capabilities
from mcp.server.fastmcp import Context      # Use `ctx: Context` as function param to get mcp context
from core.utils.state import global_state   # Use to add and read global vars
from core.utils.logger import logger        # Use to import the logger instance

def add_numbers_tool(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

## Adding Middleware To MCP Server Requests

1. Create middleware class in `app/middleware` folder as shown in the example:

```
# app/middleware/MyMiddleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from mcp.server.fastmcp import Context      # Use `ctx: Context` as function param to get mcp context
from core.utils.logger import logger        # Use to add logging capabilities
from core.utils.state import global_state   # Use to add and read global vars

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, *args, **kwargs
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        """ Your code here """

        response = await call_next(request)
        return response

```

2. Create app/config/app.py file if it does not exist and add your middlewares:

```
# app/config/app.py

MIDDLEWARE = {"mcp": [{"middleware": "app.middleware.MyMiddleware", "priority": 1}]}

# optionally, you can pass arguments to the middleware

{
    "middleware": "app.middleware.MyMiddleware",
    "priority": 1,
    "args": {
        "some_arg": "some value"
    }
}
```
