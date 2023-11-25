from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.database import get_users
from plugins import bot as app
from Config import config

@app.on_message(filters.command("broadcast") & filters.user(config.OWNER_ID))
async def broadcast(client: Client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]

        users = get_users()

        for user_id in users:
            try:
                sent_message = await client.send_message(user_id, text)
                if "can_pin_messages" in sent_message.chat_permissions:
                    await client.pin_chat_message(user_id, sent_message.id)
                print(f"Broadcast sent to user: {user_id}")
            except Exception as e:
                print(f"Failed to send broadcast to user {user_id}: {e}")

        await message.reply_text(f"Broadcast sent to {len(users)} users.")
    except IndexError:
        await message.reply_text("Invalid command format. Use /broadcast message.")
    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong.")
