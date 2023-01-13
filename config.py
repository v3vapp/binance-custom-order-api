
from dotenv import load_dotenv
load_dotenv()

import os
WEBHOOK_PASSPHRASE = os.getenv('WEBHOOK_PASSPHRASE')

apiKey = os.getenv('binance_apiKey')
secretKey = os.getenv('binance_secretKey')

testapiKey = os.getenv('binance_testapiKey')
testsecretKey = os.getenv('binance_testsecretKey')

discord_webhook = os.getenv('discord_webhook')
