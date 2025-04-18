import asyncio
import logging
from app.bot.bot import start_bot
import app.log  # logging config

logger = logging.getLogger(__name__)


async def main():
    """Main entry point of the application"""
    try:
        # Start bot
        logger.info("Starting bot...")
        await start_bot()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())