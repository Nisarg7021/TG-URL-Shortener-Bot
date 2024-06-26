from aiohttp import web
from plugins import web_server

import asyncio
import datetime
import logging
import logging.config
import sys

from pyrogram import Client

from config import *
from database import *
from helpers import temp
from pyrogram import *
from pyrogram.errors.exceptions.not_acceptable_406 import *
from database.users import *
from database.users import filter_users
from aiohttp import *
from helpers import *
from pyshorteners import *

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



class Bot(Client):
    def __init__(self):
        super().__init__(
            "shortener",
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
            plugins=dict(root="plugins")
        )


    async def start(self):
        await super().start()
        if UPDATE_CHANNEL:
            try:
                self.invite_link = await self.create_chat_invite_link(UPDATE_CHANNEL)
            except Exception:
                logging.error(f"Make sure to make the bot in your update channel {UPDATE_CHANNEL}")
                sys.exit(1)
  
        
        me = await self.get_me()
        self.owner = await self.get_users(int(OWNER_ID))
        self.username = f'@{me.username}'
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        temp.BOT_USERNAME = me.username
        temp.FIRST_NAME = me.first_name
   
        banned_users = await filter_users({"banned": True})
        async for user in banned_users:
            temp.BANNED_USERS.append(user["user_id"])
        logging.info(LOG_STR)
        await self.broadcast_admins('** Bot started successfully **\n\nBot By @GreyMattersTech')
        logging.info('Bot started')

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
      
    async def broadcast_admins(self, message):
        for admin_id in ADMINS:
            await self.send_message(admin_id, message)



async def main():
    app = Bot()
    await app.start()
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
