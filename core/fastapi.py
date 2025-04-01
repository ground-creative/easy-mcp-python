import uvicorn
from fastapi import FastAPI
from core.mcp_server import mcp
from core.utils.env import EnvConfig
from core.utils.services import load_services
from core.utils.middleware import load_middleware


# Main FastAPI application
app = FastAPI()

# Load services into the main app
load_services(app)

# Create the SSE app for MCP
sse_app = mcp.sse_app()

# Load MCP middleware for the SSE app
load_middleware(sse_app, "mcp")

# Mount the MCP SSE server inside FastAPI
app.mount("/", sse_app)


def run_fastapi():
    # logger.info("Starting FastAPI Server")
    uvicorn.run(app, host=EnvConfig.HOST, port=EnvConfig.PORT)


if __name__ == "__main__":
    run_fastapi()
