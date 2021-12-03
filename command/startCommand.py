from telegram import Update
from telegram.ext import CallbackContext

#################################
# Handles any '/start' commands #
#################################

# Set up function to handle actions when user says 'start'  
def start_wrapper():      
    def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Fridget here. Let's get started!")
    return start