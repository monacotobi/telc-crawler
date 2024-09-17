import asyncio
import os

from aiohttp import web

from code.telegram import start_bot
from code.utils.utils import logger
from code.telegram.webhook import handle_webhook

def create_app():
    app = web.Application()
    app.router.add_post('/webhook/telc', handle_webhook)
    return app

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logger.error(f'An Exception occured: {e}')

    app = create_app()
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))