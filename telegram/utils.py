from config import tg_config
from utils import logger

async def verify_secret_token(request):
    #Access the X-Telegram-Bot-Api-Secret-Token header
    received_secret_token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    TG_SECRET = tg_config.TELEGRAM_SECRET
    token_verified = received_secret_token == TG_SECRET
    if not token_verified:
        logger.error(f'Telegram token not verified: {received_secret_token}')
    return token_verified

def validate_webhook_data(data:dict, required_keys:list) -> bool:
    for key in required_keys:
        keys = key.split('.')
        current_data = data
        
        try:
            for k in keys:
                if isinstance(current_data, dict) and k in current_data and current_data[k] is not None:
                    current_data = current_data[k]
                else:
                    return False
        except KeyError as k:
            logger.error(f'A KeyError was raised: {k}', exc_info=True)
            return False
        except IndexError as i:
            logger.error(f'An IndexError was raised: {i}', exc_info=True)
            return False
        except TypeError as t:
            logger.error(f'A TypeError was raised: {t}', exc_info=True)
            return False
        except Exception as e:
            logger.error(f'An Exception was raised: {e}', exc_info=True)
            return False
                
    return True
