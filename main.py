import asyncio
import os

from aiohttp import web
from dotenv import load_dotenv

from telegram import start_bot
from utils import logger


if os.path.exists('.env'):
    load_dotenv('.env')

USER = os.getenv('USER')

def create_app():
    app = web.Application()
    app.router.add_post('webhook/telc', handle_webhook)
    return app

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logger.error(f'An Exception occured: {e}')

    app = create_app()
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))