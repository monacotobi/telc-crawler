import aiohttp
from telegram import Bot

from config import tg_config
from utils import logger

TG_TOKEN = tg_config.TELEGRAM_TOKEN
TG_SECRET = tg_config.TELEGRAM_SECRET
TG_WEBHOOK = tg_config.TELEGRAM_WEBHOOK

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token)
        self.api_url = f'https://api.telegram.org/bot{token}/'

    async def set_webhook(self, url, secret_token):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url + "setWebhook", 
                data={"url": url, 'secret_token': secret_token}
            ) as response: 
                response_data = await response.json()
                logger.info(f'Set webhook respose: {response_data}')
                return response_data
                
    async def send_message(self, user_id, text):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url + "sendMessage",
                    data={"chat_id": user_id, "text": text}
                ) as response:
                    # Check if the response status is OK
                        if response.status == 403:
                            logger.error(f'Forbidden error occurred for user {user_id}: {response},', exc_info=True)
                            raise Exception(f'User {user_id} may have blocked the bot.')
                        if response.status != 200:
                            raise aiohttp.ClientResponseError(
                                request_info=response.request_info,
                                history = response.history,
                                status = response.status
                            )
                        
                        try:
                            response_data = await response.json()
                            return response_data
                        except aiohttp.ContentTypeError:
                            # Handle case where response is not JSON
                            raise ValueError(f'Response is not in JSON format: {response}. Response format: {type(response)}')
        except aiohttp.ClientError as e:
            # This handles connection errors and all aiohttp-specific exceptions
            logger.error(f"An aiohttp ClientError occurred: {e}", exc_info=True)
            raise
        except aiohttp.ClientTimeout as e:
            # This handles the case where the request times out
            logger.error(f'An aiohttp ClientTimeout occured: {e}', exc_info=True)
            raise
        except Exception as e:
            # This handles any other unexpected errors
            logger.error(f'An Exception occured: {e}', exc_info=True)
            raise

# Initialize bot
bot = TelegramBot(TG_TOKEN)

async def start_bot():
    response = await bot.set_webhook(TG_WEBHOOK, TG_SECRET)
    if response['ok']:
        logger.info('Webhook successfully set.')
    else:
        logger.error(f'Failed to set webhook: {response['description']}')