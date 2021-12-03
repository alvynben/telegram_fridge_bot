from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

#################################
#  Handles any '/rm' commands  #
#################################

PICK_ITEM = 0

def rm_wrapper(foodList):
    def rm(update: Update, context: CallbackContext) -> int:
        """Finds and displays a list of possible items user may want to remove, and asks to pick the one to remove"""
        name = context.args[0] # TODO: Handle incorrect input

        matchingItemsText = foodList.getMatchingItemsByNameAsString(name)
        headerText = "Which item would you like to remove?:\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=headerText+matchingItemsText)

        return PICK_ITEM
    return rm

def pick_item_wrapper(foodList):
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
    return pick_item

def cancel_wrapper():
    def cancel(update: Update, context: CallbackContext) -> int:
        """Cancels and ends the conversation"""
        context.bot.send_message(chat_id=update.effective_chat.id, text='The conversation has been cancelled!')

        return ConversationHandler.END
    return cancel