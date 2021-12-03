from telegram import Update
from telegram.ext import CallbackContext

#################################
#    Handles any other text     #
#################################

def unknown_wrapper():
    def unknown(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    return unknown