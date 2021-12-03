from telegram import Update
from telegram.ext import CallbackContext

#################################
#  Handles any '/caps' commands #
#################################

def caps_wrapper():
    def caps(update: Update, context: CallbackContext):
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    return caps