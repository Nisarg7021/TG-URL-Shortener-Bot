import logging
from config import *
import asyncio
from database.users import *
from pyrogram import *
from pyrogram.types import *
from bot import *
from pyrogram.errors.exceptions.bad_request_400 import *
import shortener
from shortener import *
from pyshorteners import *

logger = logging.getLogger(__name__)

async def force_subs(client, message, channel, ft):
    owner = client.owner
    if channel:
        invite_link = client.invite_link
        try:
            user = await client.get_chat_member(channel, message.from_user.id)
            if user.status == "kicked":
                await message.reply_text("**Hey you are banned 😜**", quote=True)
                return
        except UserNotParticipant:
            buttons = [
                [InlineKeyboardButton(text='Updates Channel 🔖', url=invite_link.invite_link)],
                [InlineKeyboardButton('🔄 Refresh', callback_data='sub_refresh')]
            ]
            await message.reply_text(
                f"Hey {message.from_user.mention(style='md')}, you need to join my updates channel in order to use me 😉\n\n"
                "__Press the following button to join now 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            logger.exception(f"Exception in force_subs: {e}")
            await message.reply_text(f"Something went wrong. Please try again later or contact {owner.mention(style='md')}", quote=True)
            return
    await message.continue_propagation()

# Private Chat
@Client.on_message(filters.private)
async def private_link_handler(c: Client, message: Message):
    try:
        Fsub = await force_subs(c, message, UPDATE_CHANNEL, f"Due To Overload Only Channel Subscribers can Use the Bot Join - @GreyMattersTech")
        if Fsub:
            return
        user = await get_user(message.from_user.id)
        ban = user["banned"]
        if ban is not False:
            await message.reply_text('You Are Banned')
            return
        if message.text and message.text.startswith('/'):
            return
        caption = message.text.html if message.text else message.caption.html
        if len(await extract_link(caption)) <= 0 and not message.reply_markup:
            return
        user_method = user["method"]
        vld = await user_api_check(user)
        if vld is not True:
            return await message.reply_text(vld)
        
        txt = await message.reply('`Converting.......`', quote=True)
        await mains_convertor_handlers(message, user_method, user=user)
        await update_stats(message, user_method)
        bin_caption = f"""{caption}

#NewPost
From User :- {message.from_user.mention} [`{message.from_user.id}`]"""

        try:
            if LOG_CHANNEL and message.media:
                await message.copy(LOG_CHANNEL, bin_caption)
            elif message.text and LOG_CHANNEL:
                await c.send_message(LOG_CHANNEL, bin_caption, disable_web_page_preview=True)
        except PeerIdInvalid as e:
            logging.error("Make sure that the bot is admin in your log channel")
        finally:
            await txt.delete()
            
    except Exception as e:
        logger.exception("Exception in private_link_handler", exc_info=True)
