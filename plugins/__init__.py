from aiohttp import web
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from Config import config
import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = "tgfilestoringbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

class bot(Client):
    def __init__(self):
        super().__init__(
            name="store bot",
            api_hash=config.API_HASH,
            api_id=config.API_ID,
            plugins={
                "root": "plugins.modules"
            },
            workers=config.BOT_WORKERS,
            bot_token=config.BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(config.DB_CHANNEL)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make sure the bot is an admin in the DB Channel, and double-check the DB_CHANNEL  Value. Current Value: {config.DB_CHANNEL}")
            self.LOGGER(__name__).info("\nBot Stopped.")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nt.me/TgBotsNetwork")
        self.LOGGER(__name__).info(""" \n\n       
 _____ ____   ____   ___ _____ ____    _   _ _____ _______        _____  ____  _  __
|_   _/ ___| | __ ) / _ \_   _/ ___|  | \ | | ____|_   _\ \      / / _ \|  _ \| |/ /
  | || |  _  |  _ \| | | || | \___ \  |  \| |  _|   | |  \ \ /\ / / | | | |_) | ' / 
  | || |_| | | |_) | |_| || |  ___) | | |\  | |___  | |   \ V  V /| |_| |  _ <| . \ 
  |_| \____| |____/ \___/ |_| |____/  |_| \_|_____| |_|    \_/\_/  \___/|_| \_\_|\_\ """)
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
