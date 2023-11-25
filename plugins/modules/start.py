from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions import UserNotParticipant
from plugins import bot
from plugins.database import add_user
from plugins.modules.post import decode, DISABLE_CHANNEL_BUTTON
from plugins.modules.link import get_messages
import os
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode
import asyncio 

start_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Help", callback_data="help"),
    InlineKeyboardButton("About", callback_data="about")
    ],[
    InlineKeyboardButton("Db Channel", url="t.me/tgfilestoring"),
    ],[
    InlineKeyboardButton("Updates Channel", url="t.me/TgBotsNetwork")
]])

about_keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("⇦Back", callback_data="start")
]])

help_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⇦Back", callback_data="start")]])

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    add_user(message.from_user.id)
    text = message.text

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        try:
            string = await decode(base64_string)
            argument = string.split("-")

            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = list(range(start, end + 1))

            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]

            temp_msg = await message.reply("Please wait...")

            try:
                messages = await get_messages(client, ids)
            except Exception as e:
                await message.reply_text(f"Error getting messages: {e}")
                return

            await temp_msg.delete()

            for msg in messages:
                if bool(CUSTOM_CAPTION) and bool(msg.document):
                    caption = CUSTOM_CAPTION.format(
                        previouscaption="" if not msg.caption else msg.caption.html,
                        filename=msg.document.file_name
                    )
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                except Exception as e:
                    await message.reply_text(f"Error copying message: {e}")

        except Exception as e:
            await message.reply_text(f"Error decoding base64 string: {e}")

    else:
        await message.reply_text(
            f"Hello {message.from_user.mention}\n\nI am a private files save bot. "
            "I can save private files on certain channels, and other users can access them from a special link.",
            reply_markup=start_keyboard
        )
        
@bot.on_callback_query(filters.regex("about"))
async def about_callback(_, callback_query):
    await callback_query.edit_message_text(
        text="<b><u>About</u></b>\n\n"
             "<b>➺Bot Name:</b> <a href='http://t.me/Tgfilestoringbot'>TG FILE STORING BOT</a>\n"
             "<b>➺Language:</b> <a href='https://python.org'>python</a>\n"
             "<b>➺Library:</b> <a href='https://pyrogram.org'>pyrogram</a>\n"
             "<b>➺Developed By:</b> <a href='http://t.me/my_name_is_nobitha'>Nobitha</a>",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=about_keyboard,
    )

@bot.on_callback_query(filters.regex("start"))
async def start_callback(_, callback_query):
    await callback_query.edit_message_text(
        text=f"Hello {callback_query.message.from_user.mention}\n\nI am a private files save bot. "
             "I can save private files on certain channels, and other users can access them from a special link.",
        reply_markup=start_keyboard,
    )

@bot.on_callback_query(filters.regex("help"))
async def help_callback(_, callback_query):
    await callback_query.edit_message_text(
        text="Welcome to <a href='http://t.me/Tgfilestoringbot'>TG FILE STORING BOT</a> Send any type of media, and I'll generate a special link for you.\n\n"
             "Commands:\n"
             "/start - Start using the bot\n"
             "/help - Display this help message\n"
             "<u><b>Admin commands</b></u>\n"
             "/broadcast - Broadcast a message to all users\n"
             "/stats - Display bot statistics\n"
             "/batch - Perform batch operations\n"
             "/genlink - Generate a special link for a file\n"
             "/delfile - Delete saved special link from database\n\n"
             "<u><b>Note:</b></u> if you want access admin commands by a premium membership",
        reply_markup=help_keyboard
    )

@bot.on_message(filters.command("help") & filters.private)
async def help(_, message: Message):
    await message.reply_text(
        "Welcome to <a href='http://t.me/Tgfilestoringbot'>TG FILE STORING BOT</a> Send any type of media, and I'll generate a special link for you.\n\n"
        "Commands:\n"
        "/start - Start using the bot\n"
        "/help - Display this help message\n"
        "<u><b>Admin commands</b></u>\n"
        "/broadcast - Broadcast a message to all users\n"
        "/stats - Display bot statistics\n"
        "/batch - Perform batch operations\n"
        "/genlink - Generate a special link for a file\n"
        "/delfile - Delete saved special link from database\n\n"
        "<u><b>Note:</b></u> if you want access admin commands by a premium membership",
        reply_markup=help_keyboard
    )
