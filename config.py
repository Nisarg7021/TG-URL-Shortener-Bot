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

# Mandatory variables for the bot to start
PORT= os.environ.get("PORT", "8080")
API_ID = int(os.environ.get("API_ID", "")) #API ID from https://my.telegram.org/auth
API_HASH = os.environ.get("API_HASH", "") #API Hash from https://my.telegram.org/auth
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # Bot token from @BotFather
BOT_USERNAME = os.environ.get("BOT_USERNAME","")
ADMINS = [int(i.strip()) for i in os.environ.get("ADMINS").split(",")] if os.environ.get("ADMINS") else [] #Keep thia empty otherwise bot will not work for owner.
ADMIN = ADMINS
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Greylinks")
DATABASE_URL = os.environ.get("DATABASE_URL", "") # mongodb uri from https://www.mongodb.com/
OWNER_ID =  int(os.environ.get("OWNER_ID", "")) # id of the owner
ADMINS.append(OWNER_ID) if OWNER_ID not in ADMINS else []
Fsub = os.environ.get('Fsub', "False")
#  Optionnal variables
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "")) # log channel for information about users
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "GreyMattersTech") # For Force Subscription
BROADCAST_AS_COPY = os.environ.get('BROADCAST_AS_COPY', "False") # true if forward should be avoided
WELCOME_IMAGE = os.environ.get("WELCOME_IMAGE", 'https://telegra.ph/file/19eeb26fa2ce58765917a.jpg') # image when someone hit /start
LINK_BYPASS = "True" 
IS_PRIVATE = is_enabled(os.environ.get("IS_PRIVATE", 'False'), 'False')

#  Heroku Config for Dynos stats
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None) # your heroku account api from https://dashboard.heroku.com/account/applications
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None) # your heroku app name
HEROKU = bool(HEROKU_API_KEY and HEROKU_APP_NAME)

LOG_STR = "\nHeroku is {0}\n".format("Enabled" if HEROKU else "Disabled") + "Users {0} use this bot".format("cannot" if IS_PRIVATE else "can")
