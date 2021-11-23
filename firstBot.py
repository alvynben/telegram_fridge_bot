# Handles HTTP requests to Telegram Bot
from telegram.ext import Updater, dispatcher

# Classes to store important info regarding messages sent
from telegram import Update
from telegram.ext import CallbackContext  

# Handles Commands / Messages
from telegram.ext import CommandHandler, MessageHandler

# Filters messages for useful data
from telegram.ext import Filters

# Logging to track errors on server
import logging

# A Food Item class to store food info
from foodItem import FoodItem

# An itemList to store Food Items inside
from itemList import ItemList

# Storage Helper
from storage import Storage

# Import constants from config.py file
import config

# Create new itemList
foodList = ItemList()

# Load stored items into itemList
storage = Storage()
for item in storage.load():
    foodList.add(FoodItem(item['name'],item['expiry']))

# Set up reference to bot using API
updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Set up basic logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#################################
# Handles any '/start' commands #
#################################

# Set up function to handle actions when user says 'start'                   
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fridget here. Let's get started!")

# Creates a command handler to receive /start commands and call the start function
start_handler = CommandHandler('start', start)

# Stores the command handler in the dispatcher
dispatcher.add_handler(start_handler)

#################################
#  Handles any '/add' commands  #
#################################

def add(update: Update, context: CallbackContext):
    name, expiry = context.args

    newItem = FoodItem(name,expiry)
    foodList.add(newItem)
    storage.save(foodList.getList())

    updatedFoodListText = foodList.getListAsString()
    successText = "Great. Fridget looks like this now:\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=successText+updatedFoodListText)

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

#################################
#    Handles any other text     #
#################################

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

#################################
#  Handles any '/caps' commands #
#################################

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# Start the Bot

updater.start_polling()