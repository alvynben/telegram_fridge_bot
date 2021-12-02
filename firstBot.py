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
from foodItem import FoodItem

# An itemList to store Food Items inside
from itemList import ItemList

# Import constants from config.py file
import config

# Import OS to manage PORT stuff
import os

PORT = int(os.environ.get('PORT', 5000))

# Create new itemList
foodList = ItemList()

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

    updatedFoodListText = foodList.getListAsString('n')
    successText = "Great. Fridget looks like this now:\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=successText+updatedFoodListText)

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

#################################
#  Handles any '/rm' commands  #
#################################

PICK_ITEM = 0

def rm(update: Update, context: CallbackContext) -> int:
    """Finds and displays a list of possible items user may want to remove, and asks to pick the one to remove"""
    name = context.args[0] # TODO: Handle incorrect input

    matchingItemsText = foodList.getMatchingItemsByNameAsString(name)
    headerText = "Which item would you like to remove?:\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=headerText+matchingItemsText)

    return PICK_ITEM

def pick_item(update: Update, context: CallbackContext) -> int:
    """Tries to remove item, and informs user about success/failure"""
    index = update.message.text
    removedItem = foodList.getByIndex(index)
    
    if (removedItem == 0 or not foodList.removeByIndex(index)):
        failureText = 'The operation has failed. Please try again.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=failureText)
    else:
        successText = 'The following item has been removed:\n' + str(removedItem)
        context.bot.send_message(chat_id=update.effective_chat.id, text=successText)

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation"""
    context.bot.send_message(chat_id=update.effective_chat.id, text='The conversation has been cancelled!')

    return ConversationHandler.END

rm_handler = ConversationHandler(
    entry_points=[CommandHandler('rm',rm)],
    states={
        PICK_ITEM: [MessageHandler(Filters.text & ~Filters.command, pick_item)],
    },
    fallbacks=[CommandHandler('cancel',cancel)],
)
dispatcher.add_handler(rm_handler)

#################################
#  Handles any '/list' commands  #
#################################

def listnow(update: Update, context: CallbackContext):
    if context.args:
        sortType = context.args[0]
    else:
        sortType = 'n'

    updatedFoodListText = foodList.getListAsString(sortType)
    successText = "Fridget looks like this now:\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=successText+updatedFoodListText)

listnow_handler = CommandHandler('list', listnow)
dispatcher.add_handler(listnow_handler)

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
    
updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=config.API_KEY, webhook_url="https://lit-cove-82245.herokuapp.com/" + config.API_KEY)
 
updater.idle()