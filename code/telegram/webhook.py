from aiohttp import web

from code.utils.utils import logger
from code.crawler.crawler import crawl
from code.telegram.utils import verify_secret_token, validate_webhook_data, extract_webhook_data
from code.telegram import bot
USERS = [1579152065]
COMMANDS = ['/check']

async def handle_webhook(request):
    logger.info('Telegram webhook handler started')
    try:
        # Verify secret token
        if not await verify_secret_token(request):
            return web.Response(status=403, text='Telegram token not verified')
        
        data = await request.json()
        
        # Vakudate webhook data
        keys = ['update_id', 'message.message_id', 'message.from.id', 'message.chat', 'message.date']
        if not validate_webhook_data(data=data, required_keys=keys):
            return web.Response(status=400, text='Bad Request: Invalid Data')
        
        # Handle webhook data
        await process_webhook(data=data)

        return web.Response(status=200, text='OK')
    
    except Exception as e:
        logger.error(f'An exception occured: {e}', exc_info=True)
        return web.Response(status=500, text=f'Internal Server Error: {e}')
    

async def process_webhook(data):
    webhook_data = await extract_webhook_data(data=data)
    user_id = webhook_data['id']

    if user_id not in USERS:
        return
    
    if webhook_data['message'] not in COMMANDS:
        message = f'Please use the /check command to check for results.'
        await bot.send_message(user_id=user_id, text=message)

    messages = crawl()
    if messages:
        for message in messages:
            await bot.send_message(user_id=user_id, text=message)