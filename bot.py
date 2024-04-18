import asyncio
import logging
from pyrogram import Client
from plugins import web_server
from config import BOT_TOKEN, API_ID, API_HASH, OWNER_ID, PORT
from database import db, filter_users
from helpers import temp
from pyrogram import *
from pyrogram.errors.exceptions.not_acceptable_406 import *
from config import *
from database import *
from database.users import *
from aiohttp import *
from helpers import *
from pyshorteners import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "shortener",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=5,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.owner = await self.get_users(int(OWNER_ID))
        self.username = f'@{me.username}'
        temp.BOT_USERNAME = me.username
        temp.FIRST_NAME = me.first_name
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        if not await db.get_bot_stats():
            await db.create_stats()
        banned_users = await filter_users({"banned": True})
        async for user in banned_users:
            temp.BANNED_USERS.append(user["user_id"])
        logging.info(LOG_STR)
        await self.broadcast_admins('** Bot started successfully **\n\nBot By @GreyMattersTech')
        logging.info('Bot started')

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")


async def main():
    app = Bot()
    await app.start()


if __name__ == "__main__":
    asyncio.run(main())


