import asyncio

from code.crawler.crawler import crawl
from code.telegram import bot
from code.utils.config import USERS
from code.utils.utils import logger

async def scheduler():
    logger.info('Starting scheduler')
    messages = crawl()
    results = ['🥳 14.09.2024: SCHON DA', '🥳 14.09.2024: B1 SCHON DA']
    for user_id in USERS:
        for message in messages:
            logger.info(f'Sending message to {user_id}: {message}')
            if message in results:
                await bot.send_message(user_id=user_id, text=message)

if __name__ == "__main__":
    asyncio.run(scheduler())
