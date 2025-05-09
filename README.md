# Easy MCP Python

A simple python framework to work with mcp servers.<br>
The framework uses a fastapi application to create services.

## Applications

Here are few applications using the mvc container:<br>

[GitHub Tools](https://github.com/ground-creative/easy-mcp-github-tools-python)<br>
[Google Drive Tools](https://github.com/ground-creative/easy-mcp-gdrive-tools-python)<br>
[Gmail Tools](https://github.com/ground-creative/easy-mcp-gmail-tools-python)<br>

## Middlewares

[Google oAuth](https://github.com/ground-creative/easy-mcp-google-auth-middleware)

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

4. Clone the core repository:

```
git clone https://github.com/ground-creative/easy-mcp-core-python.git core
```

5. Install requirements:

```
pip install -r core/requirements.txt
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
```

Otionally, you can pass arguments to the middleware:

```
class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app, some_arg, *args, **kwargs
    ):
        self._some_arg = some_arg
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        """ Your code here """

        response = await call_next(request)
        return response

{
    "middleware": "app.middleware.MyMiddleware",
    "priority": 1,
    "args": {
        "some_arg": "some value"
    }
}
```

## StartUp Hook Usage

1. Create a hook in app/utils folder:

```
# app/utils/my_prestart_hook

import sqlite3
from core.utils.logger import logger        # Use to add logging capabilities
from core.utils.state import global_state   # Use to add and read global vars
from core.utils.env import EnvConfig        # Use to get env variables

def init_db(server_name):
    db_path = EnvConfig.get("DB_PATH")
    db_handler = DatabaseHandler(db_path)
    global_state.set("db_handler", db_handler)          # make db_handler available globally
    logger.info("Database initialized successfully.")
```

2. Create app/config/app.py file if it does not exist and add your hooks:

```
# app/config/app.py

PRESTART_HOOKS = {
    "fastapi": ["app.utils.my_prestart_hook.init_db"],
}
```

## Adding Services

1. Create your services in app/services folder:

```
# app/services/my_services.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from core.utils.env import EnvConfig            # Use to get env variables
from core.utils.logger import logger            # Use to add logging capabilities
from core.utils.state import global_state       # use to add and read global vars

router = APIRouter()


@router.get("/my-route")
async def my_route():
    html_content = (
        f"<h1>{EnvConfig.get("SERVER_NAME")}</h1>" f"<p>Test service working</p>"
    )
    return HTMLResponse(html_content)

```

2. Create app/config/app.py file if it does not exist and add your services:

```
SERVICES = [
    "app.services.my_services",
]
```

### Using the server info html page:

If you want to use the server info page, create app/config/app.py file if it does not exist and add this service:

```
SERVICES = [
    "core.services.server_info",    # server info html page
]

# Optional, add configuration for the info server
INFO_SERVICE_CONFIG = {
    "service_uri": "/", # the uri for the info service page
    "login_url": "'Full path to authentication URL'",
    "site_url": "Full path application main site URL",
    "site_name": "Application main site name",
    "show_tools_specs": True,   # show specs for tools (name, description, parameters)
    "header_params": {}, # a set of header parameters to document in the info page. ex: {"X-ACCESS_TOKEN": "Some description"}
    "notes": [], # a list of notes for the server information
    "privacy_policy_url": "'Privacy Policy URL'"
    "terms_of_service_url": "'Terms of Service URL'"
}

# Optionally, add a logo and favicon urls to the env file

SERVICES_LOGO_URL=http://yourdomain.com/your_logo.jpg
SERVICES_FAVICON_URL=http://yourdomain.com/your_favicon.png
```

### Server info page specs decorators

It's possible to use decorators to add tags to tools specs and to exclude tools from the specs:

```
from core.utils.tools import doc_tag, doc_name

@doc_tag("Files")               # add tag for info page specs
@doc_name("Create File")        # add custom tool name for info page specs
def create_file_tool()



from core.utils.tools import doc_exclude

doc_exclude   # exclude tool from specs info page
def edit_file_tool()
```

## Using Global Variables

To use global variables, simply import the GlobalState class:

```
from core.utils.state import global_state

def some_tool():
    all = global_state.get_all()
    var = global_state.get("some-var")
    global_state.set("some_var", "somevalue", True) # The last parameter edits value if key already exists when set to true
```

## Using Environment Variables

To get environment variables added in the .env, use `EnvConfig` utility:

```
from core.utils.env import EnvConfig

var = EnvConfig.get("VARIABLE_NAME")
```

## Using Config Variables

To get config variables added in app/config/app.py you can use the config object:

```
from core.utils.config import config

var = config.get("VARIABLE_NAME")

all = config.get_all()
```

## Folder Structure

The following folder structure is expected from the core:

```
app/
    config/         # config folder
    middleware/     # mcp middleware
    services/       # fastapi services
    tools/          # tools folder
    templates/      # templates folder
    static/         # static folder
    utils/          # utils folder
```

## Storage

Use the storage folder to store static data such as databases or images.

## Sample Application

You can find a sample application here:<br>
https://github.com/ground-creative/easy-mcp-python-test-app
