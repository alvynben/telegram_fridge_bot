from telegram import Update
from telegram.ext import CallbackContext

#################################
#  Handles any '/list' commands #
#################################
def listnow_wrapper(foodList):
    def listnow(update: Update, context: CallbackContext):
        if context.args:
            sortType = context.args[0]
        else:
            sortType = 'n'

        updatedFoodListText = foodList.getListAsString(sortType)
        successText = "Fridget looks like this now:\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=successText+updatedFoodListText)
    return listnow