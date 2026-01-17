"""Core functionality for the sustainability project."""

import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logger = logging.getLogger(__name__)


def initialize() -> None:
    """Initialize the application."""
    # Load environment variables
    env_file = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_file)
    logger.info("Application initialized")


def main() -> None:
    """Main entry point for the application."""
    initialize()
    logger.info("Starting sustainability project")
    # Add your main logic here


if __name__ == "__main__":
    main()
