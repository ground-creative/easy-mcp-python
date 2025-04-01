import argparse
from core.fastapi import run_fastapi
from core.mcp_server import run_fastmcp
from core.utils.logger import logger
from core.utils.hooks import pre_start_hook


def start_fastapi():
    """Start the FastAPI server."""
    logger.info("Starting FastAPI server...")
    run_fastapi()


def start_fastmcp():
    """Start the FastMCP server."""
    logger.info("Starting FastMCP server...")
    run_fastmcp()


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Choose which server to start.")
    parser.add_argument(
        "-s",
        "--server",
        choices=["fastapi", "fastmcp"],
        required=True,
        help="Specify which server to start: 'fastapi' or 'fastmcp'",
    )
    args = parser.parse_args()

    # Execute pre-start hook based on the selected server
    if args.server == "fastapi":
        logger.info("Selected server: FastAPI")
        pre_start_hook("fastapi")  # Call the pre-start hook
        start_fastapi()
    elif args.server == "fastmcp":
        logger.info("Selected server: FastMCP")
        pre_start_hook("fastmcp")  # Call the pre-start hook
        start_fastmcp()
