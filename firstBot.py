# Handles HTTP requests to Telegram Bot
from telegram.ext import Updater, dispatcher

# Classes to store important info regarding messages sent
from telegram import Update
from telegram.ext import CallbackContext  

# Handles Commands / Messages
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler

# Filters messages for useful data
from telegram.ext import Filters

# Logging to track errors on server
import logging

# A Food Item class to store food info
from data.foodItem import FoodItem

# An itemList to store Food Items inside
from data.itemList import ItemList

# Import OS to manage PORT stuff
import os

# Import all handlers
from command.addCommand import add_wrapper
from command.startCommand import start_wrapper
from command.rmCommand import PICK_ITEM, rm_wrapper, pick_item_wrapper, cancel_wrapper
from command.listCommand import listnow_wrapper
from command.capsCommand import caps_wrapper
from command.unknownCommand import unknown_wrapper

PORT = int(os.environ.get('PORT', 5000))
API_KEY = os.environ['TELEGRAM_FRIDGE_API_KEY']

# Create new itemList
foodList = ItemList()

# Set up reference to bot using API
updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Set up basic logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Import commands and add them to dispatcher
start_handler = CommandHandler('start', start_wrapper())
dispatcher.add_handler(start_handler)

add_handler = CommandHandler('add', add_wrapper(foodList))
dispatcher.add_handler(add_handler)

rm_handler = ConversationHandler(
    entry_points=[CommandHandler('rm',rm_wrapper(foodList))],
    states={
        PICK_ITEM: [MessageHandler(Filters.text & ~Filters.command, pick_item_wrapper(foodList))],
    },
    fallbacks=[CommandHandler('cancel',cancel_wrapper())],
)
dispatcher.add_handler(rm_handler)

listnow_handler = CommandHandler('list', listnow_wrapper(foodList))
dispatcher.add_handler(listnow_handler)

unknown_handler = MessageHandler(Filters.text & (~Filters.command), unknown_wrapper())
dispatcher.add_handler(unknown_handler)

caps_handler = CommandHandler('caps', caps_wrapper())
dispatcher.add_handler(caps_handler)

# Start the Bot
    
# updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=API_KEY, webhook_url="https://lit-cove-82245.herokuapp.com/" + API_KEY)
 
# updater.idle()

updater.start_polling()