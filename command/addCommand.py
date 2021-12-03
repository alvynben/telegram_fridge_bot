from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from data.foodItem import FoodItem

#################################
#  Handles any '/add' commands  #
#################################
def add_wrapper(foodList):
    def add(update: Update, context: CallbackContext):
        try:
            args = context.args
            name = ''
            expiry = ''
            for arg in args:
                if any(char.isdigit() for char in arg):
                    expiry=arg
                else:
                    name += f"{arg} "
            name = name.strip()
            expiry = expiry.strip()
        except:
            failureText = "Sorry, your item is formatted wrongly. It should be formatted as such:\n"
            correctFormat = "\n/add burger 2021-12-13"
            context.bot.send_message(chat_id=update.effective_chat.id, text=failureText + correctFormat)
            return

        newItem = FoodItem(name,expiry)
        foodList.add(newItem)

        updatedFoodListText = foodList.getListAsString('n')
        successText = "Great. Fridget looks like this now:\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=successText+updatedFoodListText)
    
    return add