from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from plugins import bot 
from plugins.database import add_user, get_users
from plugins.database.save_files_sql import add_total_files, add_deleted_files
from Config import config

cls_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Close", callback_data="close")]]
)

@bot.on_message(filters.command("stats"))
def stats(bot, message):
    if message.from_user.id == config.OWNER_ID:
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("See Full Stats", callback_data="see_full_stats")]]
        )
        message.reply_text(
            "Click the button below to see full stats.",
            reply_markup=keyboard
        )
    else:
        message.reply_text("You are not authorized to use this command.")

@bot.on_callback_query(filters.regex("see_full_stats"))
async def see_full_stats(bot, callback_query):
    if callback_query.from_user.id == config.OWNER_ID:
        total_users = get_users()
        stats_text = (
            f"<b>Total Users:</b> <code>{total_users}</code>\n"
            f"<b>Pyrogram Version:</b> <code>{__version__}</code>\n\n"
        )
        await callback_query.edit_message_text(stats_text, reply_markup=cls_keyboard)
    else:
        await callback_query.answer("You are not authorized to use this button.", show_alert=True)
