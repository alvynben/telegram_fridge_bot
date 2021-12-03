from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from datetime import datetime

#################################
#  Handles any '/rm' commands  #
#################################

PICK_ITEM = 0

def rm_wrapper(foodList):
    def rm(update: Update, context: CallbackContext) -> int:
        """Finds and displays a list of possible items user may want to remove, and asks to pick the one to remove"""
        try:
            name = context.args[0]
        except:
            name = ''

        matchingItems = foodList.getMatchingItemsByName(name)
        
        if not matchingItems:
            failureText = "No matching items were found."
            context.bot.send_message(chat_id=update.effective_chat.id, text=failureText)
            return ConversationHandler.END
        
        keyboard = []
        for item in matchingItems:
            keyboard.append([InlineKeyboardButton(f"{item['name']} | {item['expiry'].strftime('%d %b %Y')}", callback_data=item['id'])])
        reply_markup = InlineKeyboardMarkup(keyboard)

        headerText = "Which item would you like to remove?:\n"
        update.message.reply_text(headerText,reply_markup=reply_markup)

        return PICK_ITEM
    return rm

def pick_item_wrapper(foodList):
    def pick_item(update: Update, context: CallbackContext) -> int:
        """Tries to remove item, and informs user about success/failure"""
        query = update.callback_query
        query.answer()
        index = query.data
        removedItem = foodList.getByIndex(index)
        
        if (removedItem == 0 or not foodList.removeByIndex(index)):
            failureText = 'The operation has failed. Please try again.'
            context.bot.send_message(chat_id=update.effective_chat.id, text=failureText)
        else:
            successText = 'The following item has been removed:\n' + str(removedItem)
            context.bot.send_message(chat_id=update.effective_chat.id, text=successText)

        return ConversationHandler.END
    return pick_item

def cancel_wrapper():
    def cancel(update: Update, context: CallbackContext) -> int:
        """Cancels and ends the conversation"""
        context.bot.send_message(chat_id=update.effective_chat.id, text='The conversation has been cancelled!')

        return ConversationHandler.END
    return cancel