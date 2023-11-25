from os import path, getenv
import os
from dotenv import load_dotenv

load_dotenv()



def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default



class config:

    API_ID = "14688437"
    API_HASH = "5310285db722d1dceb128b88772d53a6"
    BOT_TOKEN = "6667196156:AAHZckswSCcMm8jD4W3KYJNrUfL5JnsZFlg"
    SUDO_USERS = ["5857041668", "5810389985"]
    OWNER_ID = int(os.environ.get("OWNER_ID", "5857041668"))
    SUDO_USERS.append(OWNER_ID) if OWNER_ID not in SUDO_USERS else []
    CHANNELS = is_enabled((os.environ.get("CHANNELS", "True")), True)
    CHANNEL_ID = (
        [int(i.strip()) for i in os.environ.get("CHANNEL_ID", "-1002119954783").split(" ")]
        if os.environ.get("CHANNEL_ID")
        else []
    )
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://wvqgakoi:F2kC9dulc1CUWoHHFC1h7UqJFpMx0NO8@berry.db.elephantsql.com/wvqgakoi")  
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "TgfileStoringBot")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002119954783"))
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', "-1002119954783"))
    FILE_STORE_CHANNEL = [int(ch) for ch in (os.environ.get('FILE_STORE_CHANNEL', '-1002119954783')).split()]
    PUBLIC_FILE_STORE = is_enabled(os.environ.get('PUBLIC_FILE_STORE', "True"), True)
    BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))
