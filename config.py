import os
from dotenv import load_dotenv
from utils import logger

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    load_dotenv('.env')

env = os.getenv('ENV', 'production')

class TG_Config:
    '''TG base configuration'''
    DEBUG = False
    TESTING = False

class TG_TestingConfig(TG_Config):
    '''TG testing configuration'''
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_TEST')
    TELEGRAM_SECRET = os.getenv('TELEGRAM_SECRET')
    DEBUG = True
    TESTING = True

class TG_ProductionConfig(TG_Config):
    '''TG production configuration'''
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_SECRET = os.getenv('TELEGRAM_SECRET')
    DEBUG = False
    TESTING = False

def get_tg_config():
    use_production_tg = os.getenv('USE_PRODUCTION_TG', 'False').lower() == 'true'

    if use_production_tg:
        logger.info('Running with Production Telegram (override)')
        return TG_ProductionConfig()

    global env

    if env == 'testing':
        logger.info('Running Telegram in testing mode')
        return TG_TestingConfig()
    else:
        logger.info('Running Telegram in production mode')
        return TG_ProductionConfig()
    
tg_config = get_tg_config()