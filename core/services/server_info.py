from fastapi import APIRouter, Request
from core.utils.env import EnvConfig
from core.utils.version import version
from core.utils.config import config
from fastapi.templating import Jinja2Templates
from pathlib import Path


templates_directory = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=templates_directory)

# Create a router with a general tag for API documentation organization
router = APIRouter()


@router.get("/")
async def status(request: Request):
    """Status endpoint that returns the current server status"""

    return templates.TemplateResponse(
        "server_info.html",
        {
            "request": request,
            "version": version,
            "logo_url": config.get("SERVICES_LOGO_URL", ""),
            "mcp_server_url": f"{EnvConfig.get('MCP_SERVER_URL')}",
            "mcp_server_name": EnvConfig.get("SERVER_NAME"),
        },
    )
