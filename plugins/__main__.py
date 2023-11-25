from pyrogram import Client, filters, idle
from plugins import bot 


if __name__ == "__main__":
    print("Bot started!")
    bot().run()
    idle()
