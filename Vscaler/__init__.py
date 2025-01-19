from hydrogram import Client, filters
from logging import info, error, Formatter, FileHandler, StreamHandler, INFO, ERROR, basicConfig
from os import environ
from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values


load_dotenv('config.env')

import logging

# Create a logger
LOGGER = logging.getLogger("Vscaler")
LOGGER.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
LOGGER.addHandler(file_handler)
LOGGER.addHandler(console_handler)
# --------------Bot Version------------------
bot_verion = "1.0.0"
"""
1 - Major Update
0 - Minor Update
0 - Enchancement
"""

# ---------------Bot Variables-----------------


API_HASH = environ.get('API_HASH', ')
if len(API_HASH) == 0:
    error("API_HASH variable is missing! Exiting now")
    exit(1)


API_ID = environ.get('API_ID', '')
if len(API_ID) == 0:
    error("API_ID variable is missing! Exiting now")
    exit(1)
else:
    API_ID = int(API_ID)

TOKEN = environ.get('TOKEN', '')
if len(TOKEN) == 0:
    error("TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = ''

if DATABASE_URL:
    vsc = MongoClient(DATABASE_URL)
    db = vsc.vscale
    current_config = dict(dotenv_values('config.env'))
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    if old_config is None:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    else:
        del old_config['_id']
    if old_config and old_config != current_config:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    elif config_dict := db.settings.config.find_one({'_id': bot_id}):
        del config_dict['_id']
        for key, value in config_dict.items():
            environ[key] = str(value)
    if pf_dict := db.settings.files.find_one({'_id': bot_id}):
        del pf_dict['_id']
        for key, value in pf_dict.items():
            if value:
                file_ = key.replace('__', '.')
                with open(file_, 'wb+') as f:
                    f.write(value)
    vsc.close()
    TOKEN = environ.get('TOKEN', '')
    bot_id = TOKEN.split(':', 1)[0]
    DATABASE_URL = environ.get('DATABASE_URL', '')
else:
    config_dict = {}

DOWNLOAD_DIR = environ.get('DOWNLOAD_DIR', '')
if len(DOWNLOAD_DIR) == 0:
    DOWNLOAD_DIR = '/usr/src/app/downloads/'
elif not DOWNLOAD_DIR.endswith("/"):
    DOWNLOAD_DIR = f'{DOWNLOAD_DIR}/'

UPDATE_CHANNEL = environ.get('UPDATE_CHANNEL', '')
if len(UPDATE_CHANNEL) == 0:
    UPDATE_CHANNEL = 'https://t.me/FondnessBots'

OWNER_ID = environ.get('OWNER_ID', '')
if len(OWNER_ID) == 0:
    error("OWNER_ID variable is missing! Exiting now")
    
else:
    OWNER_ID = int(OWNER_ID)

OWNER_UNAME = environ.get('OWNER_UNAME', '')
if len(OWNER_UNAME) == 0:
    OWNER_UNAME = 'BalaPriyan'


config_dict = {'API_HASH':API_HASH,
               'API_ID':API_ID,
               'DATABASE_URL':DATABASE_URL,
               'DOWNLOAD_DIR':DOWNLOAD_DIR,
               'OWNER_ID':OWNER_ID,
               'TOKEN':TOKEN,
               'UPDATE_CHANNEL':UPDATE_CHANNEL,
               'OWNER_UNAME':OWNER_UNAME,}



#mongodb Client Initialization
vs_client = MongoClient(DATABASE_URL)
vs_db = vs_client.vscale
users = vs_db["users"]
btasks = vs_db["tasks"]


# initializing Client
bot = Client(bot_token=TOKEN,api_hash=API_HASH,api_id=API_ID,name="Vscaler")

