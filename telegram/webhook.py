from aiohttp import web

from utils import logger

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
        await handle_webhook_data(data=data)

        return web.Response(status=200, text='OK')
    
    except Exception as e:
        logger.error(f'An exception occured: {e}', exc_info=True)
        return web.Response(status=500, text=f'Internal Server Error: {e}')