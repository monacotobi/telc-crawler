import asyncio

from code.crawler.crawler import crawl
from code.telegram import bot
from code.utils.config import USERS

async def scheduler():
    messages = crawl()
    results = ['🥳 20.07.2024: SCHON DA', '🥳 20.07.2024: B1 SCHON DA']
    for user_id in USERS:
        for message in messages:
            if message in results:
                await bot.send_message(user_id=user_id, text=message)

if __name__ == "__main__":
    asyncio.run(scheduler())
